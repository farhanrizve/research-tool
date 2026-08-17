"""Research session persistence — save, load, and resume sessions."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


@dataclass
class CheckpointRecord:
    """Record of a human checkpoint interaction."""

    checkpoint_type: str
    question: str
    answer: Any
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class FindingRecord:
    """A single research finding."""

    title: str
    authors: list[str]
    year: Optional[int]
    summary: str
    source: str
    url: str = ""
    doi: str = ""
    relevance_score: float = 0.0


@dataclass
class ResearchSession:
    """Persistent research session that can be saved and resumed."""

    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    query: str = ""
    project_dir: str = "."
    depth: str = "standard"
    sources: list[str] = field(default_factory=lambda: ["arxiv", "semantic_scholar"])

    # Pipeline state
    status: str = "created"  # created | planning | discovering | analyzing | synthesizing | writing | done | failed
    plan: Optional[dict[str, Any]] = None
    findings: list[dict[str, Any]] = field(default_factory=list)
    analysis: Optional[dict[str, Any]] = None
    synthesis: Optional[dict[str, Any]] = None
    report_path: Optional[str] = None

    # Checkpoint history
    checkpoints: list[dict[str, Any]] = field(default_factory=list)

    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    error: Optional[str] = None

    def save(self, project_dir: Optional[Path] = None) -> Path:
        """Persist session to project directory."""
        proj = Path(project_dir or self.project_dir)
        proj.mkdir(parents=True, exist_ok=True)
        session_file = proj / "session.json"
        self.updated_at = datetime.now(timezone.utc).isoformat()
        session_file.write_text(
            json.dumps(asdict(self), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return session_file

    @classmethod
    def load(cls, project_dir: Path) -> ResearchSession:
        """Load a session from a project directory."""
        session_file = Path(project_dir) / "session.json"
        if not session_file.exists():
            raise FileNotFoundError(f"No session found in {project_dir}")
        data = json.loads(session_file.read_text(encoding="utf-8"))
        return cls(**data)

    @classmethod
    def create(cls, query: str, project_dir: str = ".", depth: str = "standard",
               sources: Optional[list[str]] = None) -> ResearchSession:
        """Create and save a new session."""
        session = cls(
            query=query,
            project_dir=project_dir,
            depth=depth,
            sources=sources or ["arxiv", "semantic_scholar"],
            status="created",
        )
        session.save()
        return session

    def add_checkpoint(self, checkpoint_type: str, question: str, answer: Any) -> None:
        """Record a checkpoint interaction."""
        self.checkpoints.append(asdict(CheckpointRecord(
            checkpoint_type=checkpoint_type,
            question=question,
            answer=answer,
        )))
        self.save()

    def add_findings(self, findings: list[dict[str, Any]]) -> None:
        """Add research findings to the session."""
        self.findings.extend(findings)
        self.save()

    def update_status(self, status: str, error: Optional[str] = None) -> None:
        """Update session status."""
        self.status = status
        if error:
            self.error = error
        self.save()

    def to_dict(self) -> dict[str, Any]:
        """Export session as dictionary."""
        return asdict(self)

    @property
    def elapsed_time(self) -> str:
        """Human-readable elapsed time since session creation."""
        created = datetime.fromisoformat(self.created_at)
        now = datetime.now(timezone.utc)
        delta = now - created
        minutes = int(delta.total_seconds() / 60)
        if minutes < 1:
            return "< 1 minute"
        elif minutes < 60:
            return f"{minutes} minutes"
        else:
            hours = minutes // 60
            return f"{hours}h {minutes % 60}m"
