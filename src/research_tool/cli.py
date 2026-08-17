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
session_app = typer.Typer(help="💾 Session management")
kb_app = typer.Typer(help="🗄️  Knowledge base management")

app.add_typer(lit_app, name="lit")
app.add_typer(cite_app, name="cite")
app.add_typer(extract_app, name="extract")
app.add_typer(report_app, name="report")
app.add_typer(session_app, name="session")
app.add_typer(kb_app, name="kb")


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

    orchestrator = Orchestrator(config, project_dir=project_dir)
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


# ── research session list ────────────────────────────────────
@session_app.command("list")
def session_list(
    project_dir: Path = typer.Option(".", "--dir", "-D", help="Project directory"),
) -> None:
    """📋 List research sessions."""
    from research_tool.memory.session import ResearchSession
    from research_tool.core.project import list_projects

    projects = list_projects(project_dir)
    if not projects:
        console.print("[yellow]No projects found. Use 'research init' to create one.[/]")
        return

    console.print("\n[bold cyan]Research Sessions:[/]\n")
    for p in projects:
        proj_path = Path(p.get("path", "."))
        session_file = proj_path / "session.json"
        if session_file.exists():
            session = ResearchSession.load(proj_path)
            status_icon = {
                "created": "🆕", "planning": "📋", "discovering": "🔍",
                "analyzing": "🔬", "synthesizing": "🧩", "writing": "📝",
                "done": "✅", "failed": "❌",
            }.get(session.status, "❓")
            console.print(
                f"  {status_icon} [bold]{session.id}[/] — {session.query}\n"
                f"     Status: [cyan]{session.status}[/] | Papers: {len(session.findings)} | {session.elapsed_time}\n"
            )
        else:
            console.print(f"  📁 [bold]{p.get('topic', 'Unknown')}[/] — no session data\n")


# ── research session resume ──────────────────────────────────
@session_app.command("resume")
def session_resume(
    project_dir: Path = typer.Option(".", "--dir", "-D", help="Project directory"),
) -> None:
    """▶️  Resume a previous research session."""
    from research_tool.memory.session import ResearchSession
    from research_tool.core.config import load_project_config
    from research_tool.core.orchestrator import Orchestrator

    session_file = Path(project_dir) / "session.json"
    if not session_file.exists():
        console.print("[yellow]No session found to resume.[/]")
        raise typer.Exit(1)

    session = ResearchSession.load(Path(project_dir))
    console.print(f"[cyan]Resuming session:[/] {session.id} — {session.query}")

    config = load_project_config(project_dir)
    orchestrator = Orchestrator(config, project_dir=project_dir)
    result = orchestrator.run(session.query, depth=session.depth, sources=session.sources, resume=True)

    if result:
        console.print(f"[green]✅ Session resumed and completed![/]")
    else:
        console.print("[yellow]Session could not be completed.[/]")


# ── research session status ──────────────────────────────────
@session_app.command("status")
def session_status(
    project_dir: Path = typer.Option(".", "--dir", "-D", help="Project directory"),
) -> None:
    """📊 Show detailed status of the current session."""
    from research_tool.memory.session import ResearchSession

    session_file = Path(project_dir) / "session.json"
    if not session_file.exists():
        console.print("[yellow]No active session.[/]")
        raise typer.Exit(1)

    session = ResearchSession.load(Path(project_dir))
    status_icon = {
        "created": "🆕", "planning": "📋", "discovering": "🔍",
        "analyzing": "🔬", "synthesizing": "🧩", "writing": "📝",
        "done": "✅", "failed": "❌",
    }.get(session.status, "❓")

    console.print(Panel(
        f"[bold]Session ID:[/] {session.id}\n"
        f"[bold]Query:[/] {session.query}\n"
        f"[bold]Status:[/] {status_icon} {session.status}\n"
        f"[bold]Depth:[/] {session.depth}\n"
        f"[bold]Sources:[/] {', '.join(session.sources)}\n"
        f"[bold]Papers found:[/] {len(session.findings)}\n"
        f"[bold]Checkpoints:[/] {len(session.checkpoints)}\n"
        f"[bold]Elapsed:[/] {session.elapsed_time}\n"
        f"[bold]Created:[/] {session.created_at}\n"
        f"[bold]Updated:[/] {session.updated_at}"
        + (f"\n[bold red]Error:[/] {session.error}" if session.error else ""),
        title=f"📊 Session Status — {status_icon} {session.status.upper()}",
        border_style="cyan" if session.status != "failed" else "red",
    ))


# ── research kb search ───────────────────────────────────────
@kb_app.command("search")
def kb_search(
    query: str = typer.Argument(..., help="Search query"),
    k: int = typer.Option(5, "--limit", "-k", help="Number of results"),
    project_dir: Path = typer.Option(".", "--dir", "-D", help="Project directory"),
) -> None:
    """🔍 Search the knowledge base."""
    from research_tool.memory.knowledge import KnowledgeBase

    kb = KnowledgeBase(project_dir)
    results = kb.search(query, k=k)

    if not results:
        console.print("[yellow]No results in knowledge base.[/]")
        return

    console.print(f"\n[bold cyan]Found {len(results)} results:[/]\n")
    for i, result in enumerate(results, 1):
        meta = result.get("metadata", {})
        console.print(
            f"  [bold]{i}.[/] {meta.get('title', 'Unknown')}\n"
            f"     [dim]{result.get('text', '')[:200]}...[/]\n"
            f"     [dim]Distance: {result.get('distance', '?'):.4f}[/]\n"
        )


# ── research kb stats ────────────────────────────────────────
@kb_app.command("stats")
def kb_stats(
    project_dir: Path = typer.Option(".", "--dir", "-D", help="Project directory"),
) -> None:
    """📊 Show knowledge base statistics."""
    from research_tool.memory.knowledge import KnowledgeBase

    kb = KnowledgeBase(project_dir)
    paper_count = kb.get_paper_count()
    papers = kb.get_unique_papers()

    console.print(Panel(
        f"[bold]Total chunks:[/] {paper_count}\n"
        f"[bold]Unique papers:[/] {len(papers)}\n"
        + ("\n[bold]Papers:[/]\n" + "\n".join(
            f"  • {p['title']} ({p.get('year', '?')})" for p in papers[:10]
        ) if papers else "[dim]No papers indexed yet.[/]"),
        title="🗄️  Knowledge Base Stats",
        border_style="cyan",
    ))


# ── research kb clear ────────────────────────────────────────
@kb_app.command("clear")
def kb_clear(
    project_dir: Path = typer.Option(".", "--dir", "-D", help="Project directory"),
    confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
) -> None:
    """🗑️  Clear the knowledge base."""
    from research_tool.memory.knowledge import KnowledgeBase

    if not confirm:
        confirmed = typer.confirm("Are you sure you want to clear the knowledge base?")
        if not confirmed:
            console.print("[yellow]Cancelled.[/]")
            return

    kb = KnowledgeBase(project_dir)
    kb.clear()
    console.print("[green]✅ Knowledge base cleared.[/]")


# ── research serve ───────────────────────────────────────────
@app.command("serve")
def serve(
    mode: str = typer.Option("stdio", "--mode", "-m", help="Server mode: stdio, sse, web"),
    port: int = typer.Option(8000, "--port", "-p", help="Port for SSE/Web mode"),
    host: str = typer.Option("0.0.0.0", "--host", help="Host for Web mode"),
    project_dir: Path = typer.Option(".", "--dir", "-D", help="Project directory"),
) -> None:
    """🚀 Start the MCP server or web app for AI agent integration."""
    if mode == "web":
        try:
            import uvicorn
        except ImportError:
            console.print(
                "[red]Web mode requires the 'web' extra. Install with:\n"
                "  pip install research-tool[web][/]"
            )
            raise typer.Exit(1)

        console.print(Panel(
            f"[bold green]Starting Research Tool Web Server[/]\n\n"
            f"URL: [cyan]http://{host}:{port}[/]\n"
            f"API docs: [cyan]http://{host}:{port}/docs[/]\n"
            f"Project: [dim]{project_dir}[/]\n\n"
            "[dim]Press Ctrl+C to stop.[/]",
            title="🌐 Web Server",
            border_style="green",
        ))

        from research_tool.api.app import create_app
        app_instance = create_app(project_dir=str(project_dir))
        uvicorn.run(app_instance, host=host, port=port)
    else:
        from research_tool.server import main as server_main, mcp

        console.print(Panel(
            "[bold cyan]Starting MCP Research Server[/]\n\n"
            f"Transport: [green]{mode}[/]\n"
            + (f"Port: [green]{port}[/]\n" if mode == "sse" else "")
            + "\n[dim]Other AI agents can now use this tool via MCP protocol.[/]\n"
            "[dim]Press Ctrl+C to stop.[/]",
            title="🔌 MCP Server",
            border_style="cyan",
        ))

        if mode == "sse":
            mcp.run(transport="sse", port=port)
        else:
            mcp.run(transport="stdio")


# ── Version ───────────────────────────────────────────────────
@app.command("version")
def version() -> None:
    """Show version information."""
    console.print(f"[bold cyan]Research Tool[/] v{__version__}")


if __name__ == "__main__":
    app()
