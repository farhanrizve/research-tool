"""Base agent class — all specialist agents inherit from this."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional

from research_tool.core.config import Settings, get_settings


@dataclass
class AgentResult:
    """Standardized result from any agent."""
    success: bool = True
    data: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """Abstract base class for all research agents.

    Provides common infrastructure (config, LLM access, logging)
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

    def _llm_call(self, prompt: str, system: str | None = None, **kwargs: Any) -> str:
        """Make an LLM call using LiteLLM.

        This is a convenience wrapper that all agents can use.
        """
        try:
            import litellm

            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            response = litellm.completion(
                model=self.config.llm_model,
                messages=messages,
                **kwargs,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"[LLM call failed: {e}]"

    def _log(self, message: str) -> None:
        """Log an agent message."""
        print(f"  [{self.name}] {message}")
