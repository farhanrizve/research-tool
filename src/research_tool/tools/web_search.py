"""Web search tool — search the general web for supplementary sources."""

from __future__ import annotations

from typing import Any

import httpx


def web_search(query: str, limit: int = 10) -> list[dict[str, Any]]:
    """Search the web for information related to a query.

    Uses Tavily API if configured, otherwise returns empty results.
    """
    from research_tool.core.config import get_settings

    settings = get_settings()
    if not settings.tavily_api_key:
        return []

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": settings.tavily_api_key,
        "query": query,
        "max_results": limit,
        "search_depth": "basic",
    }

    with httpx.Client(timeout=30) as client:
        resp = client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()

    return [
        {
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("content", "")[:300],
        }
        for r in data.get("results", [])
    ]
