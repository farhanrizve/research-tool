"""Paper search tool — search academic databases.

Supports:
- Semantic Scholar API (free, comprehensive)
- arXiv API (preprints)
- Web search fallback (Tavily)
"""

from __future__ import annotations

from typing import Any, Optional

import httpx


def search_literature(
    query: str,
    databases: list[str] | None = None,
    limit: int = 20,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
) -> list[dict[str, Any]]:
    """Search academic literature across multiple databases.

    Args:
        query: Search query
        databases: List of databases to search (semantic_scholar, arxiv, web)
        limit: Maximum results per database
        year_from: Filter papers from this year
        year_to: Filter papers up to this year

    Returns:
        List of paper dicts with title, authors, abstract, year, citations, url, doi
    """
    databases = databases or ["semantic_scholar"]
    all_results: list[dict[str, Any]] = []

    for db in databases:
        try:
            if db == "semantic_scholar":
                results = _search_semantic_scholar(query, limit, year_from, year_to)
            elif db == "arxiv":
                results = _search_arxiv(query, limit)
            elif db == "web":
                results = _search_web(query, limit)
            else:
                print(f"  [paper_search] Unknown database: {db}")
                results = []
            all_results.extend(results)
        except Exception as e:
            print(f"  [paper_search] {db} search failed: {e}")

    return all_results


def _search_semantic_scholar(
    query: str,
    limit: int = 20,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
) -> list[dict[str, Any]]:
    """Search Semantic Scholar API."""
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": min(limit, 100),
        "fields": "title,authors,abstract,year,citationCount,url,externalIds,publicationDate",
    }
    if year_from or year_to:
        year_range = f"{year_from or ''}-{year_to or ''}"
        params["year"] = year_range

    with httpx.Client(timeout=30, headers={"User-Agent": "ResearchTool/0.1.0"}) as client:
        resp = client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

    papers = []
    for item in data.get("data", []):
        papers.append({
            "title": item.get("title", ""),
            "authors": [a.get("name", "") for a in item.get("authors", [])],
            "abstract": item.get("abstract", ""),
            "year": item.get("year"),
            "citations": item.get("citationCount", 0),
            "url": item.get("url", ""),
            "doi": item.get("externalIds", {}).get("DOI"),
            "source": "semantic_scholar",
        })

    return papers


def _search_arxiv(query: str, limit: int = 20) -> list[dict[str, Any]]:
    """Search arXiv API."""
    import xml.etree.ElementTree as ET

    url = "https://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": min(limit, 50),
        "sortBy": "relevance",
    }

    with httpx.Client(timeout=30) as client:
        resp = client.get(url, params=params)
        resp.raise_for_status()

    # Parse Atom XML
    root = ET.fromstring(resp.text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    papers = []
    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns)
        summary = entry.find("atom:summary", ns)
        published = entry.find("atom:published", ns)
        link = entry.find("atom:id", ns)
        authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]

        year = None
        if published is not None and published.text:
            year = int(published.text[:4])

        papers.append({
            "title": (title.text or "").strip().replace("\n", " "),
            "authors": authors,
            "abstract": (summary.text or "").strip(),
            "year": year,
            "citations": 0,  # arXiv doesn't provide citation counts
            "url": link.text if link is not None else "",
            "doi": None,
            "source": "arxiv",
        })

    return papers


def _search_web(query: str, limit: int = 10) -> list[dict[str, Any]]:
    """Search web using Tavily API (if configured) or fallback."""
    from research_tool.core.config import get_settings

    settings = get_settings()
    if not settings.tavily_api_key:
        print("  [paper_search] No Tavily API key — web search skipped")
        return []

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": settings.tavily_api_key,
        "query": query,
        "max_results": limit,
        "search_depth": "advanced",
        "include_answer": False,
    }

    with httpx.Client(timeout=30) as client:
        resp = client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()

    papers = []
    for result in data.get("results", []):
        papers.append({
            "title": result.get("title", ""),
            "authors": [],
            "abstract": result.get("content", "")[:500],
            "year": None,
            "citations": 0,
            "url": result.get("url", ""),
            "doi": None,
            "source": "web",
        })

    return papers
