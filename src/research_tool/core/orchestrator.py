"""Research orchestrator — coordinates agents and the research pipeline.

The Orchestrator is the central coordinator that:
1. Parses research intent from the user
2. Plans execution steps (which agents, in what order)
3. Manages human checkpoints
4. Coordinates specialist agents
5. Assembles the final report
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from research_tool.agents.discovery import DiscoveryAgent
from research_tool.agents.analysis import AnalysisAgent
from research_tool.agents.synthesis import SynthesisAgent
from research_tool.agents.writing import WritingAgent
from research_tool.core.config import Settings, get_settings
from research_tool.ui.interactive import checkpoint
from research_tool.ui.progress import spinner


@dataclass
class ResearchResult:
    """Final output of a research run."""
    report_path: Optional[Path] = None
    papers_count: int = 0
    citations_count: int = 0
    findings: list[dict[str, Any]] = field(default_factory=list)
    sections: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ResearchPlan:
    """Structured plan for a research query."""
    query: str
    depth: str
    sources: list[str]
    sub_questions: list[str] = field(default_factory=list)
    estimated_papers: int = 20
    steps: list[str] = field(default_factory=list)


class Orchestrator:
    """Central coordinator for the research pipeline.

    Manages the flow: Query → Plan → Discovery → Analysis → Synthesis → Writing
    with human checkpoints at key decision points.
    """

    def __init__(self, config: Optional[Settings] = None):
        self.config = config or get_settings()
        self.discovery = DiscoveryAgent(self.config)
        self.analysis = AnalysisAgent(self.config)
        self.synthesis = SynthesisAgent(self.config)
        self.writing = WritingAgent(self.config)

    def run(
        self,
        query: str,
        depth: str = "standard",
        sources: list[str] | None = None,
        output_format: str = "markdown",
    ) -> ResearchResult | None:
        """Execute the full research pipeline.

        Returns ResearchResult on success, None if cancelled.
        """
        sources = sources or self.config.default_sources

        # Step 1: Create research plan
        with spinner("📋 Creating research plan..."):
            plan = self._create_plan(query, depth, sources)

        # Step 2: Human checkpoint — approve plan
        if not self.config.auto_approve:
            approved = checkpoint(
                "plan_approval",
                "📋 Research Plan",
                self._format_plan(plan),
            )
            if not approved:
                return None

        # Step 3: Discovery — find relevant papers
        with spinner("🔍 Searching for papers..."):
            papers = asyncio.get_event_loop().run_until_complete(
                self.discovery.search(plan)
            )

        # Step 4: Analysis — extract claims and findings
        with spinner("🔬 Analyzing papers..."):
            findings = asyncio.get_event_loop().run_until_complete(
                self.analysis.analyze(papers, plan)
            )

        # Step 5: Synthesis — combine findings
        with spinner("🧩 Synthesizing findings..."):
            synthesis = asyncio.get_event_loop().run_until_complete(
                self.synthesis.synthesize(findings, plan)
            )

        # Step 6: Human checkpoint — review synthesis
        if not self.config.auto_approve:
            approved = checkpoint(
                "review_synthesis",
                "🧩 Synthesis Review",
                self._format_synthesis(synthesis),
            )
            if not approved:
                return None

        # Step 7: Writing — generate report
        with spinner("📝 Generating report..."):
            report_path = asyncio.get_event_loop().run_until_complete(
                self.writing.generate(synthesis, plan, output_format)
            )

        return ResearchResult(
            report_path=report_path,
            papers_count=len(papers),
            citations_count=len([p for p in papers if p.get("doi")]),
            findings=findings,
            sections=synthesis.get("sections", []),
        )

    def _create_plan(self, query: str, depth: str, sources: list[str]) -> ResearchPlan:
        """Create a structured research plan."""
        depth_config = {
            "quick": {"papers": 10, "sub_questions": 3},
            "standard": {"papers": 25, "sub_questions": 5},
            "deep": {"papers": 50, "sub_questions": 8},
        }
        cfg = depth_config.get(depth, depth_config["standard"])

        # Generate sub-questions using LLM
        sub_questions = self._generate_sub_questions(query, cfg["sub_questions"])

        plan = ResearchPlan(
            query=query,
            depth=depth,
            sources=sources,
            sub_questions=sub_questions,
            estimated_papers=cfg["papers"],
            steps=[
                "Search academic databases",
                "Download and parse papers",
                "Extract key claims and findings",
                "Cross-reference across papers",
                "Synthesize themes and patterns",
                "Generate structured report",
                "Format citations and bibliography",
            ],
        )
        return plan

    def _generate_sub_questions(self, query: str, count: int) -> list[str]:
        """Use LLM to break down a query into sub-questions."""
        # For now, return placeholder sub-questions
        # TODO: Integrate with LiteLLM for actual generation
        return [
            f"What is the current state of research on: {query}?",
            f"What are the main challenges in: {query}?",
            f"What are the latest breakthroughs in: {query}?",
        ][:count]

    def _format_plan(self, plan: ResearchPlan) -> str:
        """Format a research plan for display."""
        lines = [
            f"[bold]Query:[/] {plan.query}",
            f"[bold]Depth:[/] {plan.depth}",
            f"[bold]Sources:[/] {', '.join(plan.sources)}",
            f"[bold]Estimated papers:[/] ~{plan.estimated_papers}",
            "",
            "[bold]Sub-questions:[/]",
        ]
        for i, q in enumerate(plan.sub_questions, 1):
            lines.append(f"  {i}. {q}")

        lines.append("")
        lines.append("[bold]Steps:[/]")
        for i, step in enumerate(plan.steps, 1):
            lines.append(f"  {i}. {step}")

        return "\n".join(lines)

    def _format_synthesis(self, synthesis: dict[str, Any]) -> str:
        """Format synthesis results for display."""
        lines = [
            f"[bold]Papers analyzed:[/] {synthesis.get('papers_count', 0)}",
            f"[bold]Key themes:[/] {', '.join(synthesis.get('themes', []))}",
            "",
            "[bold]Summary:[/]",
            synthesis.get("summary", "No summary available."),
        ]
        return "\n".join(lines)
