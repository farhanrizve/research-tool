"""Plugin registry — loads and manages custom research tools.

Tools can be defined in code or loaded from YAML configuration.
Each tool is a callable that takes structured input and returns structured output.

Usage:
    from research_tool.plugins import ToolRegistry

    registry = ToolRegistry()
    registry.from_config(Path("research-tools.yaml"))
    result = registry.execute("pubmed_search", query="cancer", limit=10)
"""

from __future__ import annotations

import importlib
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional


@dataclass
class ToolDefinition:
    """Definition of a research tool."""

    name: str
    description: str
    handler: Callable[..., Any]
    module: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
    config: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "module": self.module,
            "parameters": self.parameters,
        }


class ToolRegistry:
    """Registry for custom research tools.

    Supports:
    - Registering tools from code
    - Loading tools from YAML configuration
    - Executing tools by name
    - Listing available tools
    """

    def __init__(self):
        self.tools: dict[str, ToolDefinition] = {}

    def register(self, name: str, handler: Callable[..., Any], description: str = "",
                 parameters: Optional[dict[str, Any]] = None) -> None:
        """Register a tool from code."""
        self.tools[name] = ToolDefinition(
            name=name,
            description=description or handler.__doc__ or "",
            handler=handler,
            parameters=parameters or {},
        )

    def from_config(self, config_path: Path) -> int:
        """Load tools from a YAML configuration file.

        Returns the number of tools loaded.
        """
        try:
            import yaml
        except ImportError:
            raise ImportError("YAML config requires PyYAML: pip install pyyaml")

        config_path = Path(config_path)
        if not config_path.exists():
            return 0

        config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        if not config or "tools" not in config:
            return 0

        count = 0
        for tool_def in config["tools"]:
            try:
                self._load_tool_from_config(tool_def)
                count += 1
            except Exception as e:
                print(f"  [plugins] Failed to load tool '{tool_def.get('name', '?')}': {e}")

        return count

    def _load_tool_from_config(self, tool_def: dict[str, Any]) -> None:
        """Load a single tool from config definition."""
        name = tool_def["name"]
        module_path = tool_def.get("module", "")
        class_name = tool_def.get("class", "")
        description = tool_def.get("description", "")
        config = tool_def.get("config", {})

        # Resolve environment variables in config
        resolved_config = {}
        for key, value in config.items():
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                env_var = value[2:-1]
                resolved_config[key] = os.environ.get(env_var, "")
            else:
                resolved_config[key] = value

        if module_path and class_name:
            # Dynamic import
            module = importlib.import_module(module_path)
            cls = getattr(module, class_name)
            instance = cls(**resolved_config) if resolved_config else cls()

            # Use the class's __call__ or a specific method
            handler = instance if callable(instance) else instance.execute

            self.tools[name] = ToolDefinition(
                name=name,
                description=description or f"Tool loaded from {module_path}.{class_name}",
                handler=handler,
                module=module_path,
                config=resolved_config,
            )
        elif "function" in tool_def:
            # Function reference (built-in tools)
            func_name = tool_def["function"]
            self.tools[name] = ToolDefinition(
                name=name,
                description=description,
                handler=self._get_builtin_handler(func_name),
                config=resolved_config,
            )
        else:
            raise ValueError(f"Tool '{name}' must have either 'module'+'class' or 'function'")

    def _get_builtin_handler(self, func_name: str) -> Callable[..., Any]:
        """Get a built-in handler by name."""
        builtins = {
            "search_arxiv": lambda **kw: self._call_search("arxiv", **kw),
            "search_semantic_scholar": lambda **kw: self._call_search("semantic_scholar", **kw),
            "search_web": lambda **kw: self._call_search("web", **kw),
        }
        if func_name in builtins:
            return builtins[func_name]
        raise ValueError(f"Unknown built-in handler: {func_name}")

    def _call_search(self, database: str, **kwargs: Any) -> list[dict[str, Any]]:
        """Helper for built-in search tools."""
        from research_tool.tools.paper_search import search_literature
        return search_literature(databases=[database], **kwargs)

    def execute(self, tool_name: str, **kwargs: Any) -> Any:
        """Execute a registered tool by name."""
        if tool_name not in self.tools:
            raise KeyError(f"Tool '{tool_name}' not found. Available: {list(self.tools.keys())}")

        tool = self.tools[tool_name]
        return tool.handler(**kwargs)

    def list_tools(self) -> list[dict[str, Any]]:
        """List all registered tools."""
        return [t.to_dict() for t in self.tools.values()]

    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        """Get a tool definition by name."""
        return self.tools.get(name)


# Global registry instance
_registry: Optional[ToolRegistry] = None


def get_registry() -> ToolRegistry:
    """Get or create the global tool registry."""
    global _registry
    if _registry is None:
        _registry = ToolRegistry()
        # Load from default config if it exists
        config_path = Path("research-tools.yaml")
        if config_path.exists():
            _registry.from_config(config_path)
    return _registry
