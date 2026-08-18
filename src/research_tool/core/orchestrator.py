"""Research orchestrator — coordinates agents and the research pipeline.

The Orchestrator is the central coordinator that:
1. Parses research intent from the user
2. Plans execution steps (which agents, in what order)
3. Manages human checkpoints
4. Coordinates specialist agents — with parallel execution
5. Indexes findings into the knowledge base (RAG)
6. Persists session state for resume capability
7. Assembles the final report
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
from research_tool.agents.prompts import ORCHESTRATOR_PLAN
from research_tool.agents.base import _cache_key, _llm_cache, CACHE_TTL
from research_tool.core.config import Settings, get_settings
from research_tool.memory.session import ResearchSession
from research_tool.memory.knowledge import KnowledgeBase
from research_tool.ui.interactive import checkpoint, checkpoint_with_options
from research_tool.ui.progress import spinner


@dataclass
class ResearchResult:
    """Final output of a research run."""
    report_path: Optional[Path] = None
    session: Optional[ResearchSession] = None
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
    project_dir: str = "."


class Orchestrator:
    """Central coordinator for the research pipeline.

    Manages the flow: Query → Plan → [Parallel Discovery] → Analysis → Synthesis → Writing
    with human checkpoints at key decision points and session persistence.
    """

    def __init__(self, config: Optional[Settings] = None, project_dir: Optional[Path] = None):
        self.config = config or get_settings()
        self.project_dir = project_dir or Path(".")
        self.discovery = DiscoveryAgent(self.config)
        self.analysis = AnalysisAgent(self.config)
        self.synthesis = SynthesisAgent(self.config)
        self.writing = WritingAgent(self.config)
        self.knowledge = KnowledgeBase(self.project_dir)

    def run(
        self,
        query: str,
        depth: str = "standard",
        sources: list[str] | None = None,
        output_format: str = "markdown",
        resume: bool = False,
    ) -> ResearchResult | None:
        """Execute the full research pipeline.

        Supports resume from a saved session. Returns ResearchResult on success, None if cancelled.
        """
        sources = sources or self.config.default_sources

        # Step 0: Create or resume session
        session_file = self.project_dir / "session.json"
        if resume and session_file.exists():
            session = ResearchSession.load(self.project_dir)
            print(f"  Resuming session {session.id} (status: {session.status})")
        else:
            session = ResearchSession.create(
                query=query,
                project_dir=str(self.project_dir),
                depth=depth,
                sources=sources,
            )

        # Step 1: Create research plan
        session.update_status("planning")
        with spinner("📋 Creating research plan..."):
            plan = self._create_plan(query, depth, sources)
        session.plan = {
            "query": plan.query,
            "depth": plan.depth,
            "sources": plan.sources,
            "sub_questions": plan.sub_questions,
            "estimated_papers": plan.estimated_papers,
        }
        session.save()

        # Step 2: Human checkpoint — approve plan
        if not self.config.auto_approve:
            approved = checkpoint(
                "plan_approval",
                "📋 Research Plan",
                self._format_plan(plan),
            )
            session.add_checkpoint("plan_approval", "Approve research plan?", approved)
            if not approved:
                session.update_status("failed", error="Plan not approved")
                return None

        # Step 3: Discovery — search in parallel across sub-questions
        session.update_status("discovering")
        with spinner("🔍 Searching for papers (parallel)..."):
            papers = self._parallel_discover(plan)

        # Deduplicate by title before indexing
        seen_titles: set[str] = set()
        unique_papers: list[dict] = []
        for paper in papers:
            key = paper.get("title", "").lower().strip()
            if key and key not in seen_titles:
                seen_titles.add(key)
                unique_papers.append(paper)
        papers = unique_papers

        # Index found papers into knowledge base
        indexed_count = 0
        for paper in papers:
            self.knowledge.index_paper(
                title=paper.get("title", ""),
                abstract=paper.get("abstract", ""),
                authors=paper.get("authors", []),
                year=paper.get("year"),
                doi=paper.get("doi", ""),
                url=paper.get("url", ""),
                source=paper.get("source", ""),
            )
            indexed_count += 1

        session.add_findings(papers)
        session.update_status("analyzing")

        # Step 4: Analysis — extract claims and findings
        with spinner("🔬 Analyzing papers..."):
            findings = self._run_async(
                self.analysis.analyze(papers, plan)
            )

        # Step 5: Synthesis — combine findings
        session.update_status("synthesizing")
        with spinner("🧩 Synthesizing findings..."):
            synthesis = self._run_async(
                self.synthesis.synthesize(findings, plan)
            )

        # Step 6: Human checkpoint — review synthesis
        if not self.config.auto_approve:
            approved = checkpoint(
                "review_synthesis",
                "🧩 Synthesis Review",
                self._format_synthesis(synthesis),
            )
            session.add_checkpoint("review_synthesis", "Approve synthesis?", approved)
            if not approved:
                session.update_status("failed", error="Synthesis not approved")
                return None

        # Step 7: Writing — generate report
        session.update_status("writing")
        with spinner("📝 Generating report..."):
            report_path = self._run_async(
                self.writing.generate(synthesis, plan, output_format)
            )

        session.report_path = str(report_path) if report_path else None
        session.update_status("done")
        session.save()

        return ResearchResult(
            report_path=report_path,
            session=session,
            papers_count=len(papers),
            citations_count=len([p for p in papers if p.get("doi")]),
            findings=findings,
            sections=synthesis.get("sections", []),
        )

    def _parallel_discover(self, plan: ResearchPlan) -> list[dict[str, Any]]:
        """Run discovery in parallel across all sub-questions.

        Uses asyncio.gather for concurrent searches, then deduplicates.
        """
        async def _search_all():
            tasks = [self.discovery.search_single(q, plan) for q in plan.sub_questions]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            all_papers = []
            for result in results:
                if isinstance(result, list):
                    all_papers.extend(result)
                elif isinstance(result, Exception):
                    print(f"  [warn] Sub-query failed: {result}")
            return all_papers

        return self._run_async(_search_all())

    def _run_async(self, coro):
        """Run an async coroutine from sync context."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Already in an event loop (e.g., Jupyter) — use nest_asyncio pattern
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    return pool.submit(asyncio.run, coro).result()
            else:
                return loop.run_until_complete(coro)
        except RuntimeError:
            return asyncio.run(coro)

    def _create_plan(self, query: str, depth: str, sources: list[str]) -> ResearchPlan:
        """Create a structured research plan."""
        depth_config = {
            "quick": {"papers": 10, "sub_questions": 3},
            "standard": {"papers": 25, "sub_questions": 5},
            "deep": {"papers": 50, "sub_questions": 8},
        }
        cfg = depth_config.get(depth, depth_config["standard"])

        sub_questions = self._generate_sub_questions(query, cfg["sub_questions"])

        plan = ResearchPlan(
            query=query,
            depth=depth,
            sources=sources,
            sub_questions=sub_questions,
            estimated_papers=cfg["papers"],
            project_dir=str(self.project_dir),
            steps=[
                "Search academic databases (parallel)",
                "Index papers into knowledge base",
                "Extract key claims and findings",
                "Cross-reference across papers",
                "Synthesize themes and patterns",
                "Generate structured report",
                "Format citations and bibliography",
            ],
        )
        return plan

    def _generate_sub_questions(self, query: str, count: int) -> list[str]:
        """Use LLM to break down a query into sub-questions.

        Falls back to template-based questions if LLM is unavailable.
        """
        try:
            result = self._llm_json(query, count=count)
            questions = result.get("sub_questions", [])
            if questions and len(questions) >= 2:
                return questions[:count]
        except Exception as e:
            print(f"  [orchestrator] LLM sub-question generation failed: {e}")

        # Fallback: template-based sub-questions
        return [
            f"What is the current state of research on: {query}?",
            f"What are the main challenges in: {query}?",
            f"What are the latest breakthroughs in: {query}?",
            f"What methodologies are used in: {query}?",
            f"What are the future directions of: {query}?",
            f"What are the practical applications of: {query}?",
            f"What are the ethical considerations of: {query}?",
            f"How does {query} compare across different domains?",
        ][:count]

    def _llm_json(self, query: str, count: int = 5) -> dict[str, Any]:
        """LLM call for plan generation using litellm directly.

        Uses OpenCode Zen free models when zen_api_key is configured.
        """
        import json
        import time
        import litellm

        system = "You are a research planning assistant. Return ONLY valid JSON."
        user = ORCHESTRATOR_PLAN.format(
            query=query,
            depth="standard",
            sources=", ".join(self.config.default_sources),
            estimated_papers=25,
        )

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

        # ── Zen free model selection ──────────────────────────────────────
        use_zen = bool(self.config.zen_api_key) and self.config.zen_free_only
        if use_zen:
            from research_tool.core.zen_provider import get_zen_provider
            zen = get_zen_provider(
                api_key=self.config.zen_api_key,
                base_url=self.config.zen_base_url,
                cache_ttl=self.config.zen_model_cache_ttl,
                preferred_model=self.config.zen_preferred_model,
            )
            litellm_kwargs = zen.get_litellm_kwargs()
            model_name = litellm_kwargs.pop("model")
        else:
            model_name = self.config.llm_model
            litellm_kwargs = {}

        # Check cache
        key = _cache_key(model_name, messages)
        if key in _llm_cache:
            cached, ts = _llm_cache[key]
            if time.time() - ts < CACHE_TTL:
                return json.loads(cached) if isinstance(cached, str) else cached

        response = litellm.completion(
            model=model_name,
            messages=messages,
            temperature=0.3,
            max_tokens=1024,
            response_format={"type": "json_object"},
            **litellm_kwargs,
        )
        text = response.choices[0].message.content or "{}"

        # Cache the result
        _llm_cache[key] = (text, time.time())

        return json.loads(text)

    def search_knowledge(self, query: str, k: int = 10) -> list[dict[str, Any]]:
        """Search the knowledge base for relevant indexed content."""
        return self.knowledge.search(query, k=k)

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
