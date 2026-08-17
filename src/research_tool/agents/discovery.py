"""Discovery Agent — finds relevant papers and sources.

Responsibilities:
- Search academic databases (Semantic Scholar, arXiv, PubMed)
- Search the web for supplementary sources
- Rank and filter results by relevance
- Return a structured list of papers
"""

from __future__ import annotations

from typing import Any

from research_tool.agents.base import AgentResult, BaseAgent
from research_tool.tools.paper_search import search_literature


class DiscoveryAgent(BaseAgent):
    """Finds and retrieves relevant research papers and sources."""

    name = "discovery"
    description = "Searches academic databases and web for relevant papers"

    async def execute(self, **kwargs: Any) -> AgentResult:
        """Execute a discovery search."""
        plan = kwargs.get("plan")
        if not plan:
            return AgentResult(success=False, errors=["No research plan provided"])

        papers = await self.search(plan)
        return AgentResult(
            success=True,
            data={"papers": papers, "count": len(papers)},
            metadata={"sources": plan.sources},
        )

    async def search(self, plan: Any) -> list[dict[str, Any]]:
        """Search across multiple sources for relevant papers."""
        all_papers: list[dict[str, Any]] = []

        for source in plan.sources:
            for question in plan.sub_questions:
                try:
                    results = search_literature(
                        question,
                        databases=[source],
                        limit=plan.estimated_papers // len(plan.sub_questions),
                    )
                    all_papers.extend(results)
                except Exception as e:
                    self._log(f"Warning: {source} search failed for '{question}': {e}")

        # Deduplicate by title
        seen = set()
        unique_papers = []
        for paper in all_papers:
            key = paper.get("title", "").lower().strip()
            if key and key not in seen:
                seen.add(key)
                unique_papers.append(paper)

        # Sort by citations (descending)
        unique_papers.sort(key=lambda p: p.get("citations", 0), reverse=True)

        self._log(f"Found {len(unique_papers)} unique papers")
        return unique_papers[:plan.estimated_papers]

    async def search_single(self, query: str, plan: Any) -> list[dict[str, Any]]:
        """Search across all sources for a single sub-question.

        Used by the orchestrator's parallel execution pattern.
        """
        all_papers: list[dict[str, Any]] = []
        limit = plan.estimated_papers // max(len(plan.sub_questions), 1)

        for source in plan.sources:
            try:
                results = search_literature(
                    query,
                    databases=[source],
                    limit=limit,
                )
                all_papers.extend(results)
            except Exception as e:
                self._log(f"Warning: {source} search failed for '{query}': {e}")

        return all_papers
