"""Synthesis Agent — combines findings into coherent themes.

Responsibilities:
- Group findings by theme/topic
- Identify patterns across papers
- Detect agreements and contradictions
- Build a narrative structure
- Generate section outlines
"""

from __future__ import annotations

from typing import Any

from research_tool.agents.base import AgentResult, BaseAgent


class SynthesisAgent(BaseAgent):
    """Synthesizes findings from multiple papers into coherent themes."""

    name = "synthesis"
    description = "Combines findings into themes, patterns, and narrative structure"

    async def execute(self, **kwargs: Any) -> AgentResult:
        """Synthesize findings."""
        findings = kwargs.get("findings", [])
        plan = kwargs.get("plan")

        result = await self.synthesize(findings, plan)
        return AgentResult(
            success=True,
            data=result,
        )

    async def synthesize(
        self, findings: list[dict[str, Any]], plan: Any
    ) -> dict[str, Any]:
        """Synthesize analysis results into structured themes."""
        # Group findings by common themes
        themes = self._identify_themes(findings)

        # Build narrative structure
        sections = self._build_sections(themes, findings, plan)

        # Generate summary
        summary = self._generate_summary(findings, themes)

        # Identify gaps
        gaps = self._identify_gaps(findings, plan)

        result = {
            "themes": [t["name"] for t in themes],
            "themes_detail": themes,
            "sections": sections,
            "summary": summary,
            "gaps": gaps,
            "papers_count": len(findings),
            "contradictions": self._find_contradictions(findings),
            "consensus_points": self._find_consensus(findings),
        }

        self._log(f"Synthesized {len(findings)} papers into {len(themes)} themes")
        return result

    def _identify_themes(self, findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Identify common themes across papers."""
        # Simple keyword-based theme identification
        # TODO: Use LLM for more sophisticated theme extraction
        theme_keywords = {
            "methodology": ["method", "approach", "framework", "algorithm", "model"],
            "performance": ["accuracy", "performance", "benchmark", "evaluation", "results"],
            "challenges": ["challenge", "limitation", "problem", "difficulty", "issue"],
            "applications": ["application", "use case", "deployment", "real-world"],
            "future_work": ["future", "direction", "open problem", "next step"],
        }

        themes = []
        for theme_name, keywords in theme_keywords.items():
            relevant = []
            for finding in findings:
                abstract = " ".join(finding.get("claims", []) + finding.get("key_findings", [])).lower()
                if any(kw in abstract for kw in keywords):
                    relevant.append(finding["title"])

            if relevant:
                themes.append({
                    "name": theme_name,
                    "papers": relevant,
                    "count": len(relevant),
                })

        # Sort by relevance (most papers first)
        themes.sort(key=lambda t: t["count"], reverse=True)
        return themes

    def _build_sections(
        self, themes: list[dict[str, Any]], findings: list[dict[str, Any]], plan: Any
    ) -> list[dict[str, Any]]:
        """Build report section outlines."""
        sections = [
            {
                "title": "Introduction",
                "level": 1,
                "content_outline": f"Overview of {plan.query} and research scope",
                "findings": [],
            },
        ]

        # Add a section for each major theme
        for theme in themes:
            sections.append({
                "title": theme["name"].replace("_", " ").title(),
                "level": 2,
                "content_outline": f"Analysis of {theme['name']} across {theme['count']} papers",
                "findings": theme["papers"],
            })

        sections.append({
            "title": "Discussion",
            "level": 1,
            "content_outline": "Synthesis of findings, implications, and future directions",
            "findings": [],
        })
        sections.append({
            "title": "Conclusion",
            "level": 1,
            "content_outline": "Summary of key insights and recommendations",
            "findings": [],
        })

        return sections

    def _generate_summary(
        self, findings: list[dict[str, Any]], themes: list[dict[str, Any]]
    ) -> str:
        """Generate an executive summary."""
        if not findings:
            return "No papers were found for analysis."

        years = [f.get("year", 0) for f in findings if f.get("year")]
        year_range = f"{min(years)}-{max(years)}" if years else "unknown"

        top_themes = ", ".join(t["name"].replace("_", " ") for t in themes[:3])

        return (
            f"This review analyzed {len(findings)} papers spanning {year_range}. "
            f"Key themes include: {top_themes}. "
            f"The analysis identified {len(themes)} major themes across the literature."
        )

    def _identify_gaps(
        self, findings: list[dict[str, Any]], plan: Any
    ) -> list[str]:
        """Identify gaps in the literature."""
        gaps = []
        if len(findings) < plan.estimated_papers * 0.5:
            gaps.append("Fewer papers found than expected — search may need broader terms")
        return gaps

    def _find_contradictions(self, findings: list[dict[str, Any]]) -> list[str]:
        """Find contradictions across papers."""
        # TODO: Use LLM to detect contradictions
        return []

    def _find_consensus(self, findings: list[dict[str, Any]]) -> list[str]:
        """Find consensus points across papers."""
        # TODO: Use LLM to detect consensus
        return []
