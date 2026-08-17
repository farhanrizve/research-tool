"""Configuration management for Research Tool."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables and config files."""

    # Paths
    project_dir: Path = Field(default=Path("."), description="Current project directory")
    data_dir: Path = Field(
        default_factory=lambda: Path(platformdirs.user_data_dir("research-tool")),
        description="Data storage directory",
    )

    # LLM
    llm_provider: str = Field(default="openai", description="LLM provider (openai, anthropic, ollama)")
    llm_model: str = Field(default="gpt-4o-mini", description="Default LLM model")
    llm_api_key: Optional[str] = Field(default=None, description="LLM API key")
    llm_base_url: Optional[str] = Field(default=None, description="Custom LLM base URL")

    # Search
    tavily_api_key: Optional[str] = Field(default=None, description="Tavily search API key")
    semantic_scholar_api_key: Optional[str] = Field(default=None, description="Semantic Scholar API key")

    # Research defaults
    default_depth: str = Field(default="standard", description="Default research depth (quick/standard/deep)")
    default_sources: list[str] = Field(
        default_factory=lambda: ["semantic_scholar", "arxiv", "web"],
        description="Default search sources",
    )
    max_concurrent_agents: int = Field(default=5, description="Max parallel agent tasks")

    # Human-in-the-loop
    auto_approve: bool = Field(default=False, description="Skip human checkpoints (for automation)")
    checkpoint_timeout: int = Field(default=300, description="Seconds to wait for human input")

    model_config = {
        "env_prefix": "RESEARCH_",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


# Module-level singleton
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def load_project_config(project_dir: Path) -> Settings:
    """Load settings with project-specific .env overrides."""
    global _settings
    env_file = project_dir / ".env"
    _settings = Settings(
        _env_file=str(env_file) if env_file.exists() else None,
        project_dir=project_dir,
    )
    return _settings
