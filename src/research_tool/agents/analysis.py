"""Analysis Agent — LLM-powered extraction of claims, methods, and findings.

Uses LLM to analyze paper metadata (title + abstract) and extract structured
information. Falls back to heuristic extraction if LLM is unavailable.
"""

from __future__ import annotations

import asyncio
from typing import Any

from research_tool.agents.base import AgentResult, BaseAgent
from research_tool.agents.prompts import format_analysis_prompt


class AnalysisAgent(BaseAgent):
    """Analyzes papers to extract structured findings using LLM."""

    name = "analysis"
    description = "Extracts claims, methods, and findings from research papers via LLM"

    # Heuristic fallback indicators (used when LLM fails)
    _claim_indicators = ["we show", "we find", "we demonstrate", "results show", "our findings"]
    _method_indicators = ["using", "via", "through", "method", "approach", "framework"]
    _finding_indicators = ["achieve", "outperform", "improve", "significant", "novel"]

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
        """Analyze papers and extract structured findings via LLM.

        Processes papers concurrently (bounded by max_concurrent_agents).
        """
        semaphore = asyncio.Semaphore(self.config.max_concurrent_agents)

        async def _analyzed(paper: dict[str, Any]) -> dict[str, Any]:
            async with semaphore:
                return await self._analyze_single(paper)

        tasks = [_analyzed(p) for p in papers]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        findings = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self._log(f"Analysis failed for paper {i}: {result}")
                # Use heuristic fallback
                findings.append(self._heuristic_extract(papers[i]))
            else:
                findings.append(result)

        self._log(f"Analyzed {len(findings)} papers ({sum(1 for f in findings if f.get('_llm_powered'))} via LLM)")
        return findings

    async def _analyze_single(self, paper: dict[str, Any]) -> dict[str, Any]:
        """Analyze a single paper using LLM."""
        title = paper.get("title", "Unknown")
        abstract = paper.get("abstract", "")

        # Skip LLM for papers with no abstract
        if not abstract or abstract == "No abstract available.":
            self._log(f"  No abstract for '{title[:50]}...' — using heuristic")
            return self._heuristic_extract(paper)

        system_prompt, user_prompt = format_analysis_prompt(paper)
        raw = await self._llm_json(user_prompt, system=system_prompt)

        if raw.get("_parse_error"):
            self._log(f"  LLM returned non-JSON for '{title[:50]}...' — using heuristic")
            return self._heuristic_extract(paper)

        # Merge LLM result with paper metadata
        result = {
            "title": title,
            "authors": paper.get("authors", []),
            "year": paper.get("year"),
            "doi": paper.get("doi"),
            "url": paper.get("url"),
            "source": paper.get("source", ""),
            "claims": raw.get("claims", []),
            "methods": raw.get("methods", []),
            "key_findings": raw.get("key_findings", []),
            "contributions": raw.get("contributions", []),
            "limitations": raw.get("limitations", []),
            "evidence_quality": raw.get("evidence_quality", "medium"),
            "evidence_reasoning": raw.get("evidence_reasoning", ""),
            "relevance_topics": raw.get("relevance_topics", []),
            "relevance_score": paper.get("relevance_score", 0.5),
            "_llm_powered": True,
        }
        return result

    def _heuristic_extract(self, paper: dict[str, Any]) -> dict[str, Any]:
        """Fallback heuristic extraction from abstract (no LLM)."""
        abstract = paper.get("abstract", "")
        sentences = [s.strip() for s in abstract.split(".") if len(s.strip()) > 20]

        claims = [s for s in sentences if any(i in s.lower() for i in self._claim_indicators)]
        methods = [s for s in sentences if any(i in s.lower() for i in self._method_indicators)]
        findings_list = [s for s in sentences if any(i in s.lower() for i in self._finding_indicators)]

        citations = paper.get("citations", 0)
        if citations > 100:
            quality = "high"
        elif citations > 20:
            quality = "medium"
        else:
            quality = "low"

        return {
            "title": paper.get("title", "Unknown"),
            "authors": paper.get("authors", []),
            "year": paper.get("year"),
            "doi": paper.get("doi"),
            "url": paper.get("url"),
            "source": paper.get("source", ""),
            "claims": claims[:5] if claims else sentences[:3],
            "methods": methods[:3],
            "key_findings": findings_list[:3] if findings_list else sentences[:2],
            "contributions": [],
            "limitations": [],
            "evidence_quality": quality,
            "evidence_reasoning": f"Based on citation count ({citations})",
            "relevance_topics": [],
            "relevance_score": paper.get("relevance_score", 0.5),
            "_llm_powered": False,
        }
