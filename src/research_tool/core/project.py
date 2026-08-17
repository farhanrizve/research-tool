"""Research project initialization and management."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


@dataclass
class ProjectInfo:
    """Information about a research project."""
    project_dir: Path
    topic: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "initialized"


def init_project(project_dir: Path, topic: str) -> ProjectInfo:
    """Initialize a new research project.

    Creates the directory structure and metadata files.
    """
    project_dir.mkdir(parents=True, exist_ok=True)

    # Create subdirectories
    (project_dir / "literatures").mkdir(exist_ok=True)
    (project_dir / "extractions").mkdir(exist_ok=True)
    (project_dir / "reports").mkdir(exist_ok=True)
    (project_dir / "notes").mkdir(exist_ok=True)

    # Create project metadata
    info = ProjectInfo(project_dir=project_dir, topic=topic)
    meta = {
        "topic": topic,
        "created_at": info.created_at,
        "status": info.status,
        "version": "0.1.0",
    }
    meta_path = project_dir / "project.json"
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    # Create .env template
    env_template = """# Research Tool — Project Environment Variables
# Copy this to .env and fill in your API keys

# LLM Provider (openai, anthropic, ollama)
RESEARCH_LLM_PROVIDER=openai
RESEARCH_LLM_MODEL=gpt-4o-mini
# RESEARCH_LLM_API_KEY=your-key-here

# Search APIs
# RESEARCH_TAVILY_API_KEY=your-key-here
# RESEARCH_SEMANTIC_SCHOLAR_API_KEY=your-key-here

# Research defaults
RESEARCH_DEFAULT_DEPTH=standard
RESEARCH_AUTO_APPROVE=false
"""
    env_path = project_dir / ".env.example"
    env_path.write_text(env_template, encoding="utf-8")

    # Create README
    readme = f"""# Research: {topic}

Initialized on {info.created_at}

## Directory Structure

- `literatures/` — Downloaded papers and PDFs
- `extractions/` — Extracted data from papers
- `reports/` — Generated research reports
- `notes/` — Your notes and annotations

## Quick Start

```bash
# Conduct research
research run "{topic}" --dir .

# Search literature
research lit search "{topic}" --dir .

# Generate report
research report generate --dir .
```

## Configuration

Copy `.env.example` to `.env` and add your API keys.
"""
    readme_path = project_dir / "README.md"
    readme_path.write_text(readme, encoding="utf-8")

    return info


def load_project(project_dir: Path) -> Optional[dict[str, Any]]:
    """Load project metadata."""
    meta_path = project_dir / "project.json"
    if meta_path.exists():
        return json.loads(meta_path.read_text(encoding="utf-8"))
    return None


def list_projects(base_dir: Path = Path(".")) -> list[dict[str, Any]]:
    """List all research projects in a directory."""
    projects = []
    for d in base_dir.iterdir():
        if d.is_dir():
            meta = load_project(d)
            if meta:
                meta["path"] = str(d)
                projects.append(meta)
    return projects
