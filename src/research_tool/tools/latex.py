"""LaTeX tool — compile and validate LaTeX documents."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional


def compile_latex(
    tex_path: Path,
    engine: str = "latexmk",
    format: str = "pdf",
) -> dict[str, any]:
    """Compile a LaTeX document.

    Args:
        tex_path: Path to the .tex file
        engine: LaTeX engine (latexmk, pdflatex, xelatex, lualatex)
        format: Output format (pdf)

    Returns:
        Dict with success status, output path, and any errors
    """
    if not tex_path.exists():
        return {"success": False, "error": f"File not found: {tex_path}"}

    cwd = tex_path.parent

    if engine == "latexmk":
        cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", tex_path.name]
    elif engine == "pdflatex":
        cmd = ["pdflatex", "-interaction=nonstopmode", tex_path.name]
    elif engine == "xelatex":
        cmd = ["xelatex", "-interaction=nonstopmode", tex_path.name]
    elif engine == "lualatex":
        cmd = ["lualatex", "-interaction=nonstopmode", tex_path.name]
    else:
        return {"success": False, "error": f"Unknown engine: {engine}"}

    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=300,
        )

        pdf_path = tex_path.with_suffix(".pdf")
        success = pdf_path.exists() and result.returncode == 0

        return {
            "success": success,
            "pdf_path": str(pdf_path) if success else None,
            "returncode": result.returncode,
            "stdout": result.stdout[-2000:] if result.stdout else "",
            "stderr": result.stderr[-2000:] if result.stderr else "",
        }

    except FileNotFoundError:
        return {"success": False, "error": f"LaTeX engine '{engine}' not found in PATH"}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Compilation timed out (5 min limit)"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def check_bibtex(tex_path: Path) -> dict[str, any]:
    """Run BibTeX to resolve citations."""
    try:
        result = subprocess.run(
            ["bibtex", tex_path.stem],
            cwd=str(tex_path.parent),
            capture_output=True,
            text=True,
            timeout=60,
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except FileNotFoundError:
        return {"success": False, "error": "bibtex not found in PATH"}
    except Exception as e:
        return {"success": False, "error": str(e)}
