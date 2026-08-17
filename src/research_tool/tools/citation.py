"""Citation management tool — BibTeX, formatting, and verification."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional


class CitationDB:
    """Simple citation database using JSON storage."""

    def __init__(self, db_path: Path = Path("citations.json")):
        self.db_path = db_path
        self.citations: list[dict[str, Any]] = self._load()

    def _load(self) -> list[dict[str, Any]]:
        if self.db_path.exists():
            return json.loads(self.db_path.read_text(encoding="utf-8"))
        return []

    def _save(self) -> None:
        self.db_path.write_text(
            json.dumps(self.citations, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def add(self, citation: dict[str, Any]) -> None:
        """Add a citation to the database."""
        citation["id"] = citation.get("id", f"cit{len(self.citations) + 1}")
        self.citations.append(citation)
        self._save()

    def find(self, query: str) -> list[dict[str, Any]]:
        """Search citations by title or author."""
        query_lower = query.lower()
        return [
            c for c in self.citations
            if query_lower in c.get("title", "").lower()
            or query_lower in c.get("author", "").lower()
        ]

    def format_all(self, style: str = "apa") -> str:
        """Format all citations in the specified style."""
        lines = []
        for c in self.citations:
            if style == "apa":
                lines.append(self._format_apa(c))
            elif style == "ieee":
                lines.append(self._format_ieee(c))
            elif style == "chicago":
                lines.append(self._format_chicago(c))
            else:
                lines.append(self._format_apa(c))
        return "\n\n".join(lines)

    def _format_apa(self, c: dict[str, Any]) -> str:
        author = c.get("author", "Unknown")
        year = c.get("year", "n.d.")
        title = c.get("title", "Untitled")
        source = c.get("source", "")
        doi = c.get("doi", "")

        result = f"{author} ({year}). {title}."
        if source:
            result += f" {source}."
        if doi:
            result += f" https://doi.org/{doi}"
        return result

    def _format_ieee(self, c: dict[str, Any]) -> str:
        author = c.get("author", "Unknown")
        title = c.get("title", "Untitled")
        source = c.get("source", "")
        year = c.get("year", "n.d.")

        result = f'{author}, "{title},"'
        if source:
            result += f" {source},"
        result += f" {year}."
        return result

    def _format_chicago(self, c: dict[str, Any]) -> str:
        author = c.get("author", "Unknown")
        title = c.get("title", "Untitled")
        source = c.get("source", "")
        year = c.get("year", "n.d.")

        result = f'{author}. "{title}."'
        if source:
            result += f" {source}"
        result += f" ({year})."
        return result

    def to_bibtex(self) -> str:
        """Export all citations as BibTeX."""
        entries = []
        for c in self.citations:
            key = c.get("id", "unknown")
            entry_type = c.get("type", "article")
            author = c.get("author", "Unknown")
            title = c.get("title", "Untitled")
            year = c.get("year", "")
            source = c.get("source", "")
            doi = c.get("doi", "")

            entry = f"@{entry_type}{{{key},\n"
            entry += f"  author = {{{author}}},\n"
            entry += f"  title = {{{title}}},\n"
            if year:
                entry += f"  year = {{{year}}},\n"
            if source:
                entry += f"  journal = {{{source}}},\n"
            if doi:
                entry += f"  doi = {{{doi}}},\n"
            entry += "}"
            entries.append(entry)

        return "\n\n".join(entries)


def add_bibtex(bibtex_path: Path) -> list[dict[str, Any]]:
    """Parse and add citations from a BibTeX file."""
    content = bibtex_path.read_text(encoding="utf-8")
    citations = _parse_bibtex(content)

    db = CitationDB()
    for c in citations:
        db.add(c)

    return citations


def _parse_bibtex(content: str) -> list[dict[str, Any]]:
    """Simple BibTeX parser."""
    import re

    entries = []
    pattern = r"@(\w+)\{([^,]+),\s*(.*?)\n\}"
    for match in re.finditer(pattern, content, re.DOTALL):
        entry_type = match.group(1)
        entry_key = match.group(2).strip()
        fields_str = match.group(3)

        fields = {}
        for field_match in re.finditer(r"(\w+)\s*=\s*\{([^}]*)\}", fields_str):
            fields[field_match.group(1).lower()] = field_match.group(2).strip()

        entries.append({
            "id": entry_key,
            "type": entry_type,
            "title": fields.get("title", ""),
            "author": fields.get("author", ""),
            "year": fields.get("year", ""),
            "source": fields.get("journal", fields.get("booktitle", "")),
            "doi": fields.get("doi", ""),
        })

    return entries
