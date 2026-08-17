"""Report rendering — terminal-based report display."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()


def display_report(report_path: Path) -> None:
    """Display a report in the terminal."""
    if not report_path.exists():
        console.print(f"[red]Report not found: {report_path}[/]")
        return

    content = report_path.read_text(encoding="utf-8")
    console.print(Markdown(content))


def display_plan(plan: dict[str, Any]) -> None:
    """Display a research plan."""
    lines = []
    lines.append(f"[bold]Query:[/] {plan.get('query', 'N/A')}")
    lines.append(f"[bold]Depth:[/] {plan.get('depth', 'N/A')}")
    lines.append(f"[bold]Sources:[/] {', '.join(plan.get('sources', []))}")
    lines.append("")

    if plan.get("sub_questions"):
        lines.append("[bold]Sub-questions:[/]")
        for i, q in enumerate(plan["sub_questions"], 1):
            lines.append(f"  {i}. {q}")

    console.print(Panel("\n".join(lines), title="📋 Research Plan", border_style="cyan"))


def display_papers(papers: list[dict[str, Any]], max_display: int = 10) -> None:
    """Display a list of papers."""
    console.print(f"\n[bold cyan]📚 Found {len(papers)} papers:[/]\n")
    for i, paper in enumerate(papers[:max_display], 1):
        console.print(
            f"  [bold]{i}.[/] {paper.get('title', 'Unknown')}\n"
            f"     [dim]{', '.join(paper.get('authors', [])[:3])} ({paper.get('year', '?')})[/]\n"
            f"     [dim]Citations: {paper.get('citations', '?')} | {paper.get('source', '')}[/]\n"
        )
    if len(papers) > max_display:
        console.print(f"  [dim]... and {len(papers) - max_display} more[/]")


def display_findings(findings: list[dict[str, Any]]) -> None:
    """Display analysis findings."""
    console.print(f"\n[bold cyan]🔬 Analysis: {len(findings)} papers analyzed[/]\n")
    for finding in findings[:5]:
        console.print(f"  [bold]{finding.get('title', 'Unknown')}[/]")
        for claim in finding.get("claims", [])[:2]:
            console.print(f"    • {claim}")
        console.print()
