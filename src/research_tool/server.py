"""MCP Server — exposes research capabilities as Model Context Protocol tools.

This server allows other AI agents (Claude Desktop, Copilot, etc.) to use
the research platform as a tool provider via the MCP protocol.

Usage:
    # Run the MCP server directly
    python -m research_tool.server

    # Or via CLI
    research serve
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

try:
    from mcp.server.mcpserver import MCPServer
except ImportError:
    try:
        from mcp.server.fastmcp import FastMCP as MCPServer  # type: ignore[assignment]
    except ImportError:
        raise ImportError(
            "MCP server requires the 'mcp' extra. Install with:\n"
            "  pip install research-tool[mcp]"
        )

from research_tool import __version__
from research_tool.core.config import load_project_config
from research_tool.core.orchestrator import Orchestrator
from research_tool.memory.knowledge import KnowledgeBase
from research_tool.memory.session import ResearchSession
from research_tool.tools.paper_search import search_literature

# Create the MCP server
mcp = MCPServer(
    "research-tool",
    instructions=(
        "AI-autonomous research platform with human-in-the-loop control. "
        "Conducts literature searches, analyzes papers, and generates reports."
    ),
)


# ── Tool: Conduct Research ──────────────────────────────────
@mcp.tool()
def research_conduct(
    query: str,
    depth: str = "standard",
    sources: str = "arxiv,semantic_scholar",
    auto: bool = False,
    project_dir: str = ".",
) -> str:
    """Conduct deep research on a topic.

    Orchestrates the full pipeline: plan → discover → analyze → synthesize → write.
    Returns a summary of findings and the report path.

    Args:
        query: Research question or topic
        depth: quick, standard, or deep
        sources: Comma-separated list of sources (arxiv, semantic_scholar, web)
        auto: Skip human checkpoints (for autonomous operation)
        project_dir: Directory to save session and report
    """
    config = load_project_config(Path(project_dir))
    config.auto_approve = auto

    source_list = [s.strip() for s in sources.split(",")]
    orchestrator = Orchestrator(config, project_dir=Path(project_dir))
    result = orchestrator.run(query, depth=depth, sources=source_list)

    if result is None:
        return "Research was cancelled or failed."

    lines = [
        f"Research complete for: {query}",
        f"Papers analyzed: {result.papers_count}",
        f"Citations: {result.citations_count}",
        f"Report: {result.report_path}",
        "",
        "Sections:",
    ]
    for section in result.sections:
        lines.append(f"  - {section.get('title', 'Untitled')}")

    if result.session:
        lines.append(f"\nSession ID: {result.session.id}")
        lines.append(f"Status: {result.session.status}")

    return "\n".join(lines)


# ── Tool: Search Literature ──────────────────────────────────
@mcp.tool()
def literature_search(
    query: str,
    databases: str = "arxiv,semantic_scholar",
    limit: int = 20,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
) -> str:
    """Search academic literature across multiple databases.

    Returns a formatted list of papers with titles, authors, years, and links.

    Args:
        query: Search query
        databases: Comma-separated databases (semantic_scholar, arxiv, web)
    limit: Maximum number of results
        year_from: Filter papers from this year
        year_to: Filter papers up to this year
    """
    db_list = [d.strip() for d in databases.split(",")]
    results = search_literature(
        query, databases=db_list, limit=limit, year_from=year_from, year_to=year_to
    )

    if not results:
        return "No results found."

    lines = [f"Found {len(results)} papers:\n"]
    for i, paper in enumerate(results, 1):
        authors = paper.get("authors", [])
        if isinstance(authors, list):
            authors_str = ", ".join(authors[:3])
            if len(authors) > 3:
                authors_str += " et al."
        else:
            authors_str = str(authors)

        lines.append(
            f"{i}. {paper.get('title', 'Unknown')}\n"
            f"   Authors: {authors_str}\n"
            f"   Year: {paper.get('year', '?')} | Citations: {paper.get('citations', 0)}\n"
            f"   URL: {paper.get('url', 'N/A')}\n"
        )

    return "\n".join(lines)


# ── Tool: Index Paper ────────────────────────────────────────
@mcp.tool()
def knowledge_index_paper(
    title: str,
    abstract: str = "",
    full_text: str = "",
    authors: str = "",
    year: Optional[int] = None,
    doi: str = "",
    url: str = "",
    source: str = "",
    project_dir: str = ".",
) -> str:
    """Index a paper into the knowledge base for semantic search.

    Args:
        title: Paper title
        abstract: Paper abstract
        full_text: Full paper text (optional, for deeper indexing)
        authors: Comma-separated author names
        year: Publication year
        doi: DOI identifier
        url: Paper URL
        source: Source database name
        project_dir: Project directory containing the knowledge base
    """
    kb = KnowledgeBase(Path(project_dir))
    author_list = [a.strip() for a in authors.split(",") if a.strip()]

    chunks = kb.index_paper(
        title=title,
        abstract=abstract,
        full_text=full_text,
        authors=author_list,
        year=year,
        doi=doi,
        url=url,
        source=source,
    )

    return f"Indexed '{title}' as {chunks} chunks. Total in KB: {kb.get_paper_count()}"


# ── Tool: Search Knowledge Base ──────────────────────────────
@mcp.tool()
def knowledge_search(
    query: str,
    k: int = 5,
    project_dir: str = ".",
) -> str:
    """Search the knowledge base using semantic similarity.

    Returns the most relevant chunks from previously indexed papers.

    Args:
        query: Search query
        k: Number of results to return
        project_dir: Project directory containing the knowledge base
    """
    kb = KnowledgeBase(Path(project_dir))
    results = kb.search(query, k=k)

    if not results:
        return "No results in knowledge base. Index papers first with knowledge_index_paper."

    lines = [f"Found {len(results)} relevant chunks:\n"]
    for i, result in enumerate(results, 1):
        meta = result.get("metadata", {})
        text = result.get("text", "")[:300]
        lines.append(
            f"{i}. [{meta.get('title', 'Unknown')}] (chunk {meta.get('chunk_idx', 0)})\n"
            f"   {text}...\n"
        )

    return "\n".join(lines)


# ── Tool: Session Status ─────────────────────────────────────
@mcp.tool()
def session_status(project_dir: str = ".") -> str:
    """Get the status of the current research session.

    Args:
        project_dir: Project directory to check
    """
    session_file = Path(project_dir) / "session.json"
    if not session_file.exists():
        return "No active session in this project."

    session = ResearchSession.load(Path(project_dir))
    lines = [
        f"Session: {session.id}",
        f"Query: {session.query}",
        f"Status: {session.status}",
        f"Depth: {session.depth}",
        f"Sources: {', '.join(session.sources)}",
        f"Papers found: {len(session.findings)}",
        f"Checkpoints: {len(session.checkpoints)}",
        f"Elapsed: {session.elapsed_time}",
        f"Created: {session.created_at}",
        f"Updated: {session.updated_at}",
    ]

    if session.error:
        lines.append(f"Error: {session.error}")

    return "\n".join(lines)


# ── Tool: Session Resume ─────────────────────────────────────
@mcp.tool()
def session_resume(project_dir: str = ".") -> str:
    """Resume a previous research session from where it left off.

    Args:
        project_dir: Project directory containing the session
    """
    session_file = Path(project_dir) / "session.json"
    if not session_file.exists():
        return "No session to resume."

    session = ResearchSession.load(Path(project_dir))
    config = load_project_config(Path(project_dir))
    config.auto_approve = True  # MCP operations are autonomous

    orchestrator = Orchestrator(config, project_dir=Path(project_dir))
    result = orchestrator.run(
        session.query, depth=session.depth, sources=session.sources, resume=True
    )

    if result:
        return f"Session resumed and completed. Report: {result.report_path}"
    return "Session could not be completed."


# ── Resource: Research Report ─────────────────────────────────
@mcp.resource("research://report/{session_id}")
def get_report(session_id: str) -> str:
    """Get the research report for a session.

    Args:
        session_id: The session ID to retrieve the report for
    """
    # Search for the session file in current directory and subdirectories
    for session_file in Path(".").rglob("session.json"):
        session = ResearchSession.load(session_file.parent)
        if session.id == session_id:
            if session.report_path:
                report_path = Path(session.report_path)
                if report_path.exists():
                    return report_path.read_text(encoding="utf-8")
                return f"Report file not found at {session.report_path}"
            return "No report generated yet for this session."
    return f"Session {session_id} not found."


# ── Resource: Knowledge Base Stats ────────────────────────────
@mcp.resource("research://kb/stats")
def kb_stats_resource() -> str:
    """Get knowledge base statistics."""
    kb = KnowledgeBase(Path("."))
    papers = kb.get_unique_papers()
    lines = [
        f"Knowledge Base Stats:",
        f"  Total chunks: {kb.get_paper_count()}",
        f"  Unique papers: {len(papers)}",
        "",
    ]
    for p in papers:
        lines.append(f"  - {p['title']} ({p.get('year', '?')})")
    return "\n".join(lines)


def main():
    """Run the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
