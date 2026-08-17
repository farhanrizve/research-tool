"""CLI entry point for the Research Tool.

Usage:
    research run "query"              # Conduct research
    research init "topic"             # Initialize project
    research lit search "query"       # Search literature
    research cite add paper.bib       # Add citation
    research extract paper.pdf        # Extract from PDF
    research report generate          # Generate report
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from research_tool import __version__

app = typer.Typer(
    name="research",
    help="🧠 AI-autonomous research platform with human-in-the-loop control",
    add_completion=False,
    rich_markup_mode="rich",
)
console = Console()

# Sub-command groups
lit_app = typer.Typer(help="📚 Literature management")
cite_app = typer.Typer(help="📖 Citation management")
extract_app = typer.Typer(help="📄 Data extraction from papers")
report_app = typer.Typer(help="📝 Report generation")

app.add_typer(lit_app, name="lit")
app.add_typer(cite_app, name="cite")
app.add_typer(extract_app, name="extract")
app.add_typer(report_app, name="report")


# ── research run ──────────────────────────────────────────────
@app.command()
def run(
    query: str = typer.Argument(..., help="Research question or topic"),
    depth: str = typer.Option("standard", "--depth", "-d", help="quick|standard|deep"),
    sources: str = typer.Option(
        "semantic_scholar,arxiv,web", "--sources", "-s", help="Comma-separated search sources"
    ),
    output: str = typer.Option("markdown", "--output", "-o", help="Output format: markdown,pdf,docx"),
    project_dir: Path = typer.Option(".", "--dir", "-D", help="Project directory"),
    auto: bool = typer.Option(False, "--auto", help="Skip human checkpoints"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """🔍 Conduct AI-powered research on any topic."""
    from research_tool.core.config import load_project_config
    from research_tool.core.orchestrator import Orchestrator

    config = load_project_config(project_dir)
    config.auto_approve = auto

    source_list = [s.strip() for s in sources.split(",")]

    console.print(Panel(
        f"[bold cyan]Research Query:[/] {query}\n"
        f"[bold cyan]Depth:[/] {depth}  |  [bold cyan]Sources:[/] {', '.join(source_list)}\n"
        f"[bold cyan]Output:[/] {output}  |  [bold cyan]Auto:[/] {auto}",
        title="🧠 Starting Research",
        border_style="cyan",
    ))

    orchestrator = Orchestrator(config)
    result = orchestrator.run(query, depth=depth, sources=source_list, output_format=output)

    if result:
        console.print(Panel(
            f"[bold green]✅ Research complete![/]\n\n"
            f"Report: [link]{result.report_path}[/link]\n"
            f"Papers analyzed: {result.papers_count}\n"
            f"Citations: {result.citations_count}",
            title="📊 Results",
            border_style="green",
        ))
    else:
        console.print("[bold red]❌ Research cancelled or failed.[/]")


# ── research init ─────────────────────────────────────────────
@app.command()
def init(
    topic: str = typer.Argument(..., help="Research topic or project name"),
    project_dir: Optional[Path] = typer.Option(None, "--dir", "-D", help="Project directory"),
) -> None:
    """📁 Initialize a new research project."""
    from research_tool.core.project import init_project

    target = project_dir or Path(topic.lower().replace(" ", "-"))
    result = init_project(target, topic)

    console.print(Panel(
        f"[bold green]✅ Project initialized![/]\n\n"
        f"Directory: [cyan]{result.project_dir}[/]\n"
        f"Topic: [cyan]{topic}[/]\n\n"
        f"Next steps:\n"
        f"  cd {result.project_dir}\n"
        f"  research run \"{topic}\"",
        title="📁 New Project",
        border_style="green",
    ))


# ── research lit search ──────────────────────────────────────
@lit_app.command("search")
def lit_search(
    query: str = typer.Argument(..., help="Search query"),
    databases: str = typer.Option(
        "semantic_scholar,arxiv", "--db", help="Comma-separated databases"
    ),
    limit: int = typer.Option(20, "--limit", "-n", help="Max results"),
    year_from: Optional[int] = typer.Option(None, "--year-from", help="Filter from year"),
    year_to: Optional[int] = typer.Option(None, "--year-to", help="Filter to year"),
) -> None:
    """🔍 Search academic literature."""
    from research_tool.tools.paper_search import search_literature

    db_list = [d.strip() for d in databases.split(",")]
    results = search_literature(query, databases=db_list, limit=limit, year_from=year_from, year_to=year_to)

    if not results:
        console.print("[yellow]No results found.[/]")
        return

    console.print(f"\n[bold cyan]Found {len(results)} papers:[/]\n")
    for i, paper in enumerate(results, 1):
        console.print(
            f"  [bold]{i}.[/] {paper['title']}\n"
            f"     [dim]{paper.get('authors', 'Unknown')} ({paper.get('year', '?')})[/]\n"
            f"     [dim]Citations: {paper.get('citations', '?')} | {paper.get('url', '')}[/]\n"
        )


# ── research lit add ─────────────────────────────────────────
@lit_app.command("add")
def lit_add(
    paper_path: Path = typer.Argument(..., help="Path to PDF or BibTeX file"),
) -> None:
    """➕ Add a paper to the literature library."""
    from research_tool.tools.pdf_parser import add_paper

    if not paper_path.exists():
        console.print(f"[red]File not found: {paper_path}[/]")
        raise typer.Exit(1)

    result = add_paper(paper_path)
    console.print(f"[green]✅ Added: {result.title}[/]")


# ── research lit review ─────────────────────────────────────
@lit_app.command("review")
def lit_review(
    topic: str = typer.Option("", "--topic", "-t", help="Review topic"),
    papers_dir: Path = typer.Option("./literatures", "--dir", help="Papers directory"),
) -> None:
    """📋 Review and summarize literature."""
    console.print(f"[cyan]Literature review for:[/] {topic or 'all papers'}")
    console.print("[dim]This will use the analysis agent to summarize papers...[/]")


# ── research cite add ────────────────────────────────────────
@cite_app.command("add")
def cite_add(
    source: Path = typer.Argument(..., help="BibTeX file or DOI"),
) -> None:
    """➕ Add a citation."""
    console.print(f"[cyan]Adding citation:[/] {source}")


# ── research cite format ─────────────────────────────────────
@cite_app.command("format")
def cite_format(
    style: str = typer.Option("apa", "--style", "-s", help="Citation style (apa, ieee, chicago)"),
    document: Optional[Path] = typer.Option(None, "--doc", help="Document to format citations in"),
) -> None:
    """📖 Format citations in a document."""
    console.print(f"[cyan]Formatting citations in style:[/] {style}")


# ── research extract ─────────────────────────────────────────
@extract_app.command("paper")
def extract_paper(
    paper_path: Path = typer.Argument(..., help="Path to PDF"),
    tables: bool = typer.Option(True, "--tables/--no-tables", help="Extract tables"),
    figures: bool = typer.Option(True, "--figures/--no-figures", help="Extract figures"),
    claims: bool = typer.Option(True, "--claims/--no-claims", help="Extract claims"),
) -> None:
    """📄 Extract structured data from a paper."""
    console.print(f"[cyan]Extracting from:[/] {paper_path}")
    console.print(f"  Tables: {'✅' if tables else '❌'}  Figures: {'✅' if figures else '❌'}  Claims: {'✅' if claims else '❌'}")


# ── research report generate ─────────────────────────────────
@report_app.command("generate")
def report_generate(
    template: str = typer.Option("article", "--template", "-t", help="Report template"),
    chapters: int = typer.Option(6, "--chapters", "-c", help="Number of chapters"),
    format: str = typer.Option("pdf", "--format", "-f", help="Output format (pdf, docx, md)"),
) -> None:
    """📝 Generate a research report."""
    console.print(f"[cyan]Generating {template} report with {chapters} chapters...[/]")


# ── Version ───────────────────────────────────────────────────
@app.command("version")
def version() -> None:
    """Show version information."""
    console.print(f"[bold cyan]Research Tool[/] v{__version__}")


if __name__ == "__main__":
    app()
