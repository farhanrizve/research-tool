"""Synthesis Agent — LLM-powered theme identification and knowledge synthesis.

Groups findings by theme, identifies patterns across papers, detects agreements
and contradictions, and builds a narrative structure for the report.
"""

from __future__ import annotations

from typing import Any

from research_tool.agents.base import AgentResult, BaseAgent
from research_tool.agents.prompts import format_synthesis_prompt


class SynthesisAgent(BaseAgent):
    """Synthesizes findings from multiple papers into coherent themes via LLM."""

    name = "synthesis"
    description = "Combines findings into themes, patterns, and narrative structure using LLM"

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
        """Synthesize analysis results into structured themes via LLM."""
        query = plan.query if hasattr(plan, "query") else str(plan)

        # Try LLM-powered synthesis
        if findings and any(f.get("_llm_powered") for f in findings):
            llm_result = await self._llm_synthesize(findings, query)
            if llm_result and not llm_result.get("_parse_error"):
                # Build sections from LLM themes
                sections = self._build_sections_from_themes(
                    llm_result.get("themes", []),
                    findings,
                    plan,
                )
                result = {
                    "themes": [t["name"] for t in llm_result.get("themes", [])],
                    "themes_detail": llm_result.get("themes", []),
                    "sections": sections,
                    "summary": self._build_summary(llm_result, findings),
                    "gaps": llm_result.get("research_gaps", []),
                    "papers_count": len(findings),
                    "contradictions": llm_result.get("contradictions", []),
                    "consensus_points": llm_result.get("cross_cutting_insights", []),
                    "methodological_trends": llm_result.get("methodological_trends", ""),
                    "temporal_trends": llm_result.get("temporal_trends", ""),
                    "_llm_powered": True,
                }
                self._log(
                    f"LLM synthesis: {len(result['themes'])} themes, "
                    f"{len(result['gaps'])} gaps identified"
                )
                return result

        # Fallback: keyword-based synthesis
        self._log("Using heuristic fallback for synthesis")
        return self._heuristic_synthesize(findings, plan)

    async def _llm_synthesize(
        self, findings: list[dict[str, Any]], query: str
    ) -> dict[str, Any] | None:
        """Run LLM-powered synthesis."""
        system_prompt, user_prompt = format_synthesis_prompt(findings, query)
        raw = await self._llm_json(user_prompt, system=system_prompt)
        if raw.get("_parse_error"):
            self._log(f"LLM returned non-JSON for synthesis: {raw.get('_raw', '')[:200]}")
            return None
        return raw

    def _build_sections_from_themes(
        self,
        themes: list[dict[str, Any]],
        findings: list[dict[str, Any]],
        plan: Any,
    ) -> list[dict[str, Any]]:
        """Convert LLM themes into report section outlines."""
        sections = []
        for i, theme in enumerate(themes):
            sections.append({
                "title": theme.get("name", f"Theme {i + 1}"),
                "level": 2,
                "content_outline": theme.get("description", ""),
                "theme_description": theme.get("description", ""),
                "findings": theme.get("paper_titles", []),
                "consensus": theme.get("consensus", ""),
                "debate": theme.get("debate", ""),
            })
        return sections

    def _build_summary(
        self, llm_result: dict[str, Any], findings: list[dict[str, Any]]
    ) -> str:
        """Build a summary from LLM synthesis results."""
        themes = llm_result.get("themes", [])
        gaps = llm_result.get("research_gaps", [])
        insights = llm_result.get("cross_cutting_insights", [])

        parts = [
            f"This review analyzed {len(findings)} papers across {len(themes)} major themes.",
        ]
        if insights:
            parts.append("Key cross-cutting insights: " + "; ".join(insights[:3]) + ".")
        if gaps:
            parts.append(f"The review identified {len(gaps)} significant research gaps.")
        return " ".join(parts)

    # ── Heuristic fallback ────────────────────────────────────────────────

    def _heuristic_synthesize(
        self, findings: list[dict[str, Any]], plan: Any
    ) -> dict[str, Any]:
        """Keyword-based synthesis fallback when LLM is unavailable."""
        themes = self._heuristic_themes(findings)
        sections = self._build_sections_from_themes(themes, findings, plan)
        gaps = self._heuristic_gaps(findings, plan)

        return {
            "themes": [t["name"] for t in themes],
            "themes_detail": themes,
            "sections": sections,
            "summary": f"Analyzed {len(findings)} papers across {len(themes)} themes.",
            "gaps": gaps,
            "papers_count": len(findings),
            "contradictions": [],
            "consensus_points": [],
            "methodological_trends": "",
            "temporal_trends": "",
            "_llm_powered": False,
        }

    def _heuristic_themes(self, findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Keyword-based theme identification."""
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
                text = " ".join(
                    finding.get("claims", [])
                    + finding.get("key_findings", [])
                ).lower()
                if any(kw in text for kw in keywords):
                    relevant.append(finding.get("title", "Unknown"))

            if relevant:
                themes.append({
                    "name": theme_name,
                    "description": f"Papers addressing {theme_name.replace('_', ' ')}",
                    "paper_titles": relevant,
                    "count": len(relevant),
                    "consensus": "",
                    "debate": "",
                })

        themes.sort(key=lambda t: t.get("count", 0), reverse=True)
        return themes

    def _heuristic_gaps(
        self, findings: list[dict[str, Any]], plan: Any
    ) -> list[str]:
        """Identify obvious gaps from limited findings."""
        gaps = []
        if len(findings) < 5:
            gaps.append("Limited number of papers found — results may not be comprehensive")
        no_abstract = sum(1 for f in findings if not f.get("abstract", "").strip())
        if no_abstract > len(findings) * 0.3:
            gaps.append(f"{no_abstract} papers lacked abstracts, limiting analysis depth")
        return gaps

    def _find_consensus(self, findings: list[dict[str, Any]]) -> list[str]:
        """Find consensus points across papers."""
        # TODO: Use LLM to detect consensus
        return []
