"""Base agent class — all specialist agents inherit from this."""

from __future__ import annotations

import asyncio
import json
import hashlib
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional

from research_tool.core.config import Settings, get_settings

# ── LLM response cache (module-level, survives across agent calls) ──────────
_llm_cache: dict[str, tuple[str, float]] = {}
CACHE_TTL = 3600  # 1 hour


def _cache_key(model: str, messages: list[dict], **kwargs: Any) -> str:
    """Generate a deterministic cache key from LLM call parameters."""
    raw = json.dumps({"model": model, "messages": messages, **kwargs}, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()[:24]


@dataclass
class AgentResult:
    """Standardized result from any agent."""
    success: bool = True
    data: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """Abstract base class for all research agents.

    Provides common infrastructure (config, LLM access, caching, logging)
    and enforces a consistent interface.
    """

    name: str = "base"
    description: str = "Base agent"

    def __init__(self, config: Optional[Settings] = None):
        self.config = config or get_settings()

    @abstractmethod
    async def execute(self, **kwargs: Any) -> AgentResult:
        """Execute the agent's task. Must be implemented by subclasses."""
        ...

    # ── LLM integration ───────────────────────────────────────────────────

    async def _llm(
        self,
        prompt: str,
        system: str | None = None,
        *,
        temperature: float = 0.3,
        max_tokens: int = 4096,
        json_mode: bool = False,
        use_cache: bool = True,
        retries: int = 2,
    ) -> str:
        """Async LLM call with caching and retry.

        Uses OpenCode Zen free models when zen_api_key is configured,
        otherwise falls back to the configured llm_model.

        Args:
            prompt: User prompt.
            system: Optional system prompt.
            temperature: Sampling temperature.
            max_tokens: Max tokens in response.
            json_mode: Request JSON output (sets response_format).
            use_cache: Whether to use the response cache.
            retries: Number of retries on failure.

        Returns:
            The model's text response.
        """
        import litellm

        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        # ── Zen free model selection ──────────────────────────────────────
        use_zen = bool(self.config.zen_api_key) and self.config.zen_free_only
        if use_zen:
            from research_tool.core.zen_provider import get_zen_provider
            zen = get_zen_provider(
                api_key=self.config.zen_api_key,
                base_url=self.config.zen_base_url,
                cache_ttl=self.config.zen_model_cache_ttl,
                preferred_model=self.config.zen_preferred_model,
            )
            litellm_kwargs = zen.get_litellm_kwargs()
            model_name = litellm_kwargs.pop("model")
            kwargs: dict[str, Any] = {
                "model": model_name,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                **litellm_kwargs,
            }
        else:
            kwargs = {
                "model": self.config.llm_model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            model_name = self.config.llm_model

        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        # Check cache
        key = _cache_key(model_name, messages, temperature=temperature, json_mode=json_mode)
        if use_cache and key in _llm_cache:
            cached, ts = _llm_cache[key]
            if time.time() - ts < CACHE_TTL:
                self._log(f"(cache hit, {len(cached)} chars)")
                return cached

        # Retry loop — on Zen, also try fallback models
        last_error: Exception | None = None
        fallback_models: list[str] = []
        if use_zen:
            from research_tool.core.zen_provider import get_zen_provider, PREFERRED_ORDER
            zen = get_zen_provider(
                api_key=self.config.zen_api_key,
                base_url=self.config.zen_base_url,
                cache_ttl=self.config.zen_model_cache_ttl,
            )
            current = zen.get_model()
            fallback_models = [m for m in PREFERRED_ORDER if m != current]

        all_models = [model_name] + [f"openai/{m}" for m in fallback_models[:3]]

        for model_attempt in all_models:
            current_kwargs = dict(kwargs)
            current_kwargs["model"] = model_attempt
            for attempt in range(retries + 1):
                try:
                    response = await litellm.acompletion(**current_kwargs)
                    text = response.choices[0].message.content or ""
                    if use_cache:
                        _llm_cache[key] = (text, time.time())
                    return text
                except Exception as e:
                    last_error = e
                    if attempt < retries:
                        wait = 2 ** attempt
                        self._log(f"LLM call failed (attempt {attempt + 1}): {e} — retrying in {wait}s")
                        await asyncio.sleep(wait)

            # Move to next fallback model
            if use_zen and model_attempt != all_models[-1]:
                self._log(f"Trying fallback model: {model_attempt}")

        # All retries exhausted
        self._log(f"LLM call failed after {retries + 1} attempts: {last_error}")
        return f"[LLM call failed: {last_error}]"

    async def _llm_json(
        self,
        prompt: str,
        system: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """LLM call that returns parsed JSON.

        Attempts json_mode first; falls back to extracting JSON from the response text.
        """
        # Try with json_mode
        raw = await self._llm(prompt, system, json_mode=True, **kwargs)
        return self._parse_json(raw)

    @staticmethod
    def _parse_json(text: str) -> dict[str, Any]:
        """Extract and parse JSON from LLM output, handling markdown fences."""
        text = text.strip()
        # Strip markdown code fences
        if text.startswith("```"):
            lines = text.split("\n")
            # Remove first line (```json or ```) and last line (```)
            lines = [l for l in lines[1:] if not l.strip().startswith("```")]
            text = "\n".join(lines).strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON object/array in the text
            for start_char, end_char in [("{", "}"), ("[", "]")]:
                start = text.find(start_char)
                end = text.rfind(end_char)
                if start != -1 and end > start:
                    try:
                        return json.loads(text[start:end + 1])
                    except json.JSONDecodeError:
                        continue
            return {"_raw": text, "_parse_error": True}

    def _log(self, message: str) -> None:
        """Log an agent message."""
        print(f"  [{self.name}] {message}")
