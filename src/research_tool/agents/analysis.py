"""Analysis Agent — extracts claims, methods, and findings from papers.

Responsibilities:
- Parse paper content (PDF or structured data)
- Extract key claims and evidence
- Identify methodologies used
- Rate evidence quality
- Build a claim-evidence graph
"""

from __future__ import annotations

from typing import Any

from research_tool.agents.base import AgentResult, BaseAgent


class AnalysisAgent(BaseAgent):
    """Analyzes papers to extract structured findings."""

    name = "analysis"
    description = "Extracts claims, methods, and findings from research papers"

    async def execute(self, **kwargs: Any) -> AgentResult:
        """Analyze a set of papers."""
        papers = kwargs.get("papers", [])
        plan = kwargs.get("plan")

        findings = await self.analyze(papers, plan)
        return AgentResult(
            success=True,
            data={"findings": findings, "count": len(findings)},
        )

    async def analyze(
        self, papers: list[dict[str, Any]], plan: Any
    ) -> list[dict[str, Any]]:
        """Analyze papers and extract structured findings."""
        findings = []

        for paper in papers:
            finding = {
                "title": paper.get("title", "Unknown"),
                "authors": paper.get("authors", []),
                "year": paper.get("year"),
                "doi": paper.get("doi"),
                "url": paper.get("url"),
                "claims": self._extract_claims(paper),
                "methods": self._extract_methods(paper),
                "key_findings": self._extract_key_findings(paper),
                "evidence_quality": self._rate_evidence(paper),
                "relevance_score": paper.get("relevance_score", 0.5),
            }
            findings.append(finding)

        self._log(f"Analyzed {len(findings)} papers")
        return findings

    def _extract_claims(self, paper: dict[str, Any]) -> list[str]:
        """Extract key claims from a paper."""
        # Use abstract as primary source of claims
        abstract = paper.get("abstract", "")
        if not abstract:
            return ["No abstract available"]

        # Simple heuristic: split into sentences and identify claim-like ones
        sentences = [s.strip() for s in abstract.split(".") if len(s.strip()) > 20]
        claim_indicators = ["we show", "we find", "we demonstrate", "results show", "our findings"]
        claims = [
            s for s in sentences
            if any(indicator in s.lower() for indicator in claim_indicators)
        ]
        return claims[:5] if claims else sentences[:3]

    def _extract_methods(self, paper: dict[str, Any]) -> list[str]:
        """Extract methods from a paper."""
        abstract = paper.get("abstract", "")
        method_indicators = ["using", "via", "through", "method", "approach", "framework"]
        sentences = [s.strip() for s in abstract.split(".") if len(s.strip()) > 20]
        methods = [
            s for s in sentences
            if any(indicator in s.lower() for indicator in method_indicators)
        ]
        return methods[:3] if methods else []

    def _extract_key_findings(self, paper: dict[str, Any]) -> list[str]:
        """Extract key findings from a paper."""
        abstract = paper.get("abstract", "")
        finding_indicators = ["achieve", "outperform", "improve", "significant", "novel"]
        sentences = [s.strip() for s in abstract.split(".") if len(s.strip()) > 20]
        key_findings = [
            s for s in sentences
            if any(indicator in s.lower() for indicator in finding_indicators)
        ]
        return key_findings[:3] if key_findings else sentences[:2]

    def _rate_evidence(self, paper: dict[str, Any]) -> str:
        """Rate evidence quality based on available signals."""
        citations = paper.get("citations", 0)
        if citations > 100:
            return "strong"
        elif citations > 20:
            return "moderate"
        elif citations > 5:
            return "preliminary"
        else:
            return "emerging"
