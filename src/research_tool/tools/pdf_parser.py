"""PDF parser tool — extract text, tables, and metadata from PDFs."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional


def add_paper(paper_path: Path) -> dict[str, Any]:
    """Add a paper to the literature library.

    Extracts metadata and stores it for later analysis.
    """
    metadata = extract_metadata(paper_path)

    # Store in literatures directory
    lit_dir = Path("literatures")
    lit_dir.mkdir(exist_ok=True)

    # Copy PDF if it's not already there
    target = lit_dir / paper_path.name
    if not target.exists():
        import shutil
        shutil.copy2(paper_path, target)

    # Save metadata as JSON
    import json
    meta_path = lit_dir / f"{paper_path.stem}.meta.json"
    meta_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    return metadata


def extract_metadata(paper_path: Path) -> dict[str, Any]:
    """Extract metadata from a PDF paper."""
    try:
        import pymupdf

        doc = pymupdf.open(str(paper_path))

        # Get basic info
        metadata = {
            "title": doc.metadata.get("title", paper_path.stem),
            "author": doc.metadata.get("author", "Unknown"),
            "subject": doc.metadata.get("subject", ""),
            "keywords": doc.metadata.get("keywords", ""),
            "pages": len(doc),
            "file_path": str(paper_path),
            "file_size": paper_path.stat().st_size,
        }

        # Extract first page text for abstract detection
        if len(doc) > 0:
            first_page_text = doc[0].get_text()
            metadata["first_page_preview"] = first_page_text[:500]

        doc.close()
        return metadata

    except ImportError:
        return {
            "title": paper_path.stem,
            "author": "Unknown",
            "file_path": str(paper_path),
            "error": "pymupdf not installed",
        }
    except Exception as e:
        return {
            "title": paper_path.stem,
            "author": "Unknown",
            "file_path": str(paper_path),
            "error": str(e),
        }


def extract_text(paper_path: Path, pages: Optional[list[int]] = None) -> str:
    """Extract full text from a PDF."""
    try:
        import pymupdf

        doc = pymupdf.open(str(paper_path))
        texts = []

        page_indices = pages or range(len(doc))
        for i in page_indices:
            if i < len(doc):
                texts.append(doc[i].get_text())

        doc.close()
        return "\n\n".join(texts)

    except ImportError:
        return "[pymupdf not installed]"
    except Exception as e:
        return f"[Error extracting text: {e}]"


def extract_tables(paper_path: Path) -> list[dict[str, Any]]:
    """Extract tables from a PDF."""
    # Simple table detection based on grid patterns
    # For production, consider using camelot-py or tabula-py
    return [{"note": "Table extraction requires camelot-py or tabula-py"}]
