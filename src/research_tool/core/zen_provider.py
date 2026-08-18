"""OpenCode Zen free model provider.

Periodically fetches the list of free models from OpenCode Zen API
and selects the best available model for LLM calls.

Free models (as of Aug 2026):
- big-pickle
- deepseek-v4-flash-free
- mimo-v2.5-free
- hy3-free
- laguna-s-2.1-free
- nemotron-3-ultra-free
- nemotron-3.5-lightning-free

All use the OpenAI-compatible chat completions endpoint:
  https://opencode.ai/zen/v1/chat/completions
"""

from __future__ import annotations

import time
import threading
from typing import Any, Optional

import httpx


# ── Known free model IDs (hardcoded fallback) ──────────────────────────────
KNOWN_FREE_MODELS: list[str] = [
    "deepseek-v4-flash-free",
    "mimo-v2.5-free",
    "big-pickle",
    "nemotron-3-ultra-free",
    "nemotron-3.5-lightning-free",
    "hy3-free",
    "laguna-s-2.1-free",
]

# Preferred model order (best → fallback)
# DeepSeek V4 Flash Free is the most capable free model
PREFERRED_ORDER: list[str] = [
    "deepseek-v4-flash-free",
    "mimo-v2.5-free",
    "nemotron-3-ultra-free",
    "nemotron-3.5-lightning-free",
    "big-pickle",
    "hy3-free",
    "laguna-s-2.1-free",
]


class ZenProvider:
    """Manages free model selection from OpenCode Zen.

    Fetches the model list from the Zen API periodically, caches it,
    and selects the best available free model.
    """

    BASE_URL = "https://opencode.ai/zen/v1"
    MODELS_ENDPOINT = f"{BASE_URL}/models"
    CHAT_ENDPOINT = f"{BASE_URL}/chat/completions"

    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
        cache_ttl: int = 3600,
        preferred_model: str | None = None,
    ):
        """Initialize the Zen provider.

        Args:
            api_key: OpenCode Zen API key.
            base_url: Override base URL (default: https://opencode.ai/zen/v1).
            cache_ttl: Seconds to cache the free models list (default: 3600 = 1hr).
            preferred_model: Force a specific free model ID (overrides auto-selection).
        """
        self.api_key = api_key
        self.base_url = (base_url or self.BASE_URL).rstrip("/")
        self.cache_ttl = cache_ttl
        self.preferred_model = preferred_model

        self._free_models: list[dict[str, Any]] = []
        self._free_model_ids: list[str] = []
        self._last_fetch: float = 0
        self._lock = threading.Lock()
        self._selected_model: str | None = None

    @property
    def models_endpoint(self) -> str:
        return f"{self.base_url}/models"

    @property
    def chat_endpoint(self) -> str:
        return f"{self.base_url}/chat/completions"

    def _is_cache_valid(self) -> bool:
        return (
            self._free_model_ids
            and (time.time() - self._last_fetch) < self.cache_ttl
        )

    def refresh_models(self) -> list[str]:
        """Fetch the free models list from Zen API.

        Returns the list of free model IDs.
        """
        with self._lock:
            # Double-check after acquiring lock
            if self._is_cache_valid():
                return self._free_model_ids

            try:
                resp = httpx.get(
                    self.models_endpoint,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=15,
                )
                resp.raise_for_status()
                data = resp.json()

                models = data.get("data", [])
                free_models = []
                for model in models:
                    # Check if model is free (pricing info or ID pattern)
                    model_id = model.get("id", "")
                    pricing = model.get("pricing", {})

                    # A model is free if:
                    # 1. It has "-free" suffix, OR
                    # 2. All pricing fields are "0" or "Free", OR
                    # 3. It's in our known free list
                    is_free = (
                        model_id.endswith("-free")
                        or model_id in KNOWN_FREE_MODELS
                        or _pricing_is_free(pricing)
                    )

                    if is_free:
                        free_models.append({
                            "id": model_id,
                            "name": model.get("name", model_id),
                            "pricing": pricing,
                        })

                self._free_models = free_models
                self._free_model_ids = [m["id"] for m in free_models]
                self._last_fetch = time.time()

                if free_models:
                    print(f"  [zen] Fetched {len(free_models)} free models from Zen API")
                else:
                    print("  [zen] No free models found from API, using hardcoded list")
                    self._free_model_ids = list(KNOWN_FREE_MODELS)

            except Exception as e:
                print(f"  [zen] Failed to fetch models from API: {e}")
                if not self._free_model_ids:
                    print("  [zen] Using hardcoded free model list as fallback")
                    self._free_model_ids = list(KNOWN_FREE_MODELS)

            # Select the best model
            self._selected_model = self._select_best()
            return self._free_model_ids

    def _select_best(self) -> str:
        """Select the best free model based on preference order."""
        if self.preferred_model:
            if self.preferred_model in self._free_model_ids:
                return self.preferred_model
            print(f"  [zen] Preferred model '{self.preferred_model}' not available")

        for model_id in PREFERRED_ORDER:
            if model_id in self._free_model_ids:
                return model_id

        # Fallback to first available
        if self._free_model_ids:
            return self._free_model_ids[0]

        return "deepseek-v4-flash-free"  # Ultimate fallback

    def get_model(self, refresh: bool = False) -> str:
        """Get the current best free model ID.

        Args:
            refresh: Force a refresh of the models list.

        Returns:
            The model ID string (e.g., 'deepseek-v4-flash-free').
        """
        if refresh or not self._is_cache_valid():
            self.refresh_models()
        return self._selected_model or "deepseek-v4-flash-free"

    def get_litellm_model(self, refresh: bool = False) -> str:
        """Get the model string for litellm (with 'openai/' prefix).

        Returns:
            e.g., 'openai/deepseek-v4-flash-free'
        """
        model = self.get_model(refresh=refresh)
        return f"openai/{model}"

    def get_litellm_kwargs(self, refresh: bool = False) -> dict[str, Any]:
        """Get the full kwargs dict for litellm.acompletion().

        Returns:
            Dict with model, api_base, api_key, and extra headers.
        """
        model = self.get_model(refresh=refresh)
        return {
            "model": f"openai/{model}",
            "api_base": self.chat_endpoint,
            "api_key": self.api_key,
            "extra_headers": {
                "User-Agent": "ResearchTool/0.2.0",
            },
        }

    def get_all_free_models(self, refresh: bool = False) -> list[str]:
        """Get all available free model IDs."""
        if refresh or not self._is_cache_valid():
            self.refresh_models()
        return list(self._free_model_ids)

    def get_status(self) -> dict[str, Any]:
        """Get provider status info."""
        return {
            "selected_model": self._selected_model,
            "available_free_models": self._free_model_ids,
            "cache_age_seconds": int(time.time() - self._last_fetch) if self._last_fetch else None,
            "cache_ttl": self.cache_ttl,
            "api_base": self.base_url,
        }


def _pricing_is_free(pricing: dict[str, Any]) -> bool:
    """Check if a pricing dict indicates a free model."""
    if not pricing:
        return False
    for key in ("prompt", "completion", "image", "request"):
        val = str(pricing.get(key, "")).strip().lower()
        if val and val not in ("0", "0.0", "0.00", "free", ""):
            return False
    return True


# ── Module-level singleton ──────────────────────────────────────────────────
_zen_provider: Optional[ZenProvider] = None


def get_zen_provider(
    api_key: str | None = None,
    base_url: str | None = None,
    cache_ttl: int = 3600,
    preferred_model: str | None = None,
) -> ZenProvider | None:
    """Get or create the global Zen provider.

    Returns None if no API key is provided.
    """
    global _zen_provider
    if not api_key:
        return None
    if _zen_provider is None:
        _zen_provider = ZenProvider(
            api_key=api_key,
            base_url=base_url,
            cache_ttl=cache_ttl,
            preferred_model=preferred_model,
        )
    return _zen_provider
