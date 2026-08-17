"""LLM prompt templates for research agents.

All prompts are defined here for easy tuning and versioning.
Each template function returns (system_prompt, user_prompt) tuples.
"""

from __future__ import annotations

from typing import Any


# ═══════════════════════════════════════════════════════════════════════════════
# ANALYSIS AGENT PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════

ANALYSIS_SYSTEM = """\
You are a rigorous academic research analyst. Your job is to extract structured \
information from research paper metadata (title, abstract, authors, year).

You must be precise, evidence-based, and avoid speculation. If information is \
not available in the provided metadata, say "Not available from abstract." \
Never fabricate claims or findings.
"""

ANALYSIS_EXTRACT = """\
Analyze the following research paper and extract structured information.

**Title:** {title}
**Authors:** {authors}
**Year:** {year}
**Abstract:**
{abstract}

Extract the following in JSON format:
{{
    "claims": [
        "List of 1-5 key claims made by the authors (directly supported by the abstract)"
    ],
    "methods": [
        "List of 1-3 methodologies, techniques, or approaches described"
    ],
    "key_findings": [
        "List of 1-5 main findings or results reported"
    ],
    "contributions": [
        "List of 1-3 novel contributions to the field"
    ],
    "limitations": [
        "List of 0-3 limitations or open problems mentioned or implied"
    ],
    "evidence_quality": "high|medium|low",
    "evidence_reasoning": "Brief explanation of evidence quality rating (1-2 sentences)",
    "relevance_topics": [
        "List of 2-5 key topics/themes this paper addresses"
    ]
}}

Be specific and use exact terminology from the paper. Return ONLY the JSON object.\
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SYNTHESIS AGENT PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════

SYNTHESIS_SYSTEM = """\
You are a senior research synthesizer. Your job is to identify patterns, themes, \
and relationships across multiple research paper analyses.

Think like a systematic review author: group findings by theme, identify areas \
of consensus and contradiction, and highlight gaps in the literature. Be analytical, \
not merely descriptive.
"""

SYNTHESIS_THEMES = """\
Given the following analyses of {count} research papers on the topic "{query}", \
identify the major themes, patterns, and relationships.

**Paper Analyses:**
{analyses_text}

Synthesize into a JSON response:
{{
    "themes": [
        {{
            "name": "Theme name (short, descriptive)",
            "description": "2-3 sentence description of this theme",
            "paper_titles": ["List of paper titles contributing to this theme"],
            "consensus": "What the literature generally agrees on",
            "debate": "Any disagreements or contradictions within this theme"
        }}
    ],
    "cross_cutting_insights": [
        "Insights that span multiple themes (2-4 items)"
    ],
    "contradictions": [
        {{
            "papers": ["Paper A title", "Paper B title"],
            "description": "What the contradiction is about"
        }}
    ],
    "research_gaps": [
        "Identified gaps or under-explored areas (2-5 items)"
    ],
    "methodological_trends": "Brief description of common methodologies used across papers",
    "temporal_trends": "How the field has evolved over time (if apparent)"
}}

Return ONLY the JSON object.\
"""


# ═══════════════════════════════════════════════════════════════════════════════
# WRITING AGENT PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════

WRITING_SYSTEM = """\
You are an expert academic writer specializing in research reports and literature \
reviews. You write clearly, precisely, and with appropriate academic tone.

Your writing should:
- Use formal academic language without being overly complex
- Present findings objectively, citing evidence from the synthesis
- Structure arguments logically with clear topic sentences
- Avoid hedging language ("it seems", "maybe") unless genuinely uncertain
- Use active voice where possible ("We find" not "It was found")
"""

WRITING_SECTION = """\
Write the "{section_title}" section of a research report.

**Research query:** {query}
**Section outline:** {outline}
**Theme description:** {theme_description}
**Key papers:** {paper_list}
**Key findings from these papers:** {findings}
**Synthesis notes:** {synthesis_notes}

Write 3-6 paragraphs (300-800 words). Include inline citations as [Author, Year] \
where supported by the provided findings. Do not fabricate citations.

Return ONLY the section text in Markdown format.\
"""

WRITING_ABSTRACT = """\
Write an abstract (150-250 words) for a research report.

**Research query:** {query}
**Depth:** {depth}
**Papers analyzed:** {paper_count}
**Major themes:** {themes}
**Key findings summary:** {summary}
**Research gaps:** {gaps}

Write a concise abstract that:
1. States the research question
2. Describes the methodology (literature review of N papers)
3. Summarizes the 3-5 most important findings
4. Notes key limitations or gaps

Return ONLY the abstract text.\
"""

WRITING_LIMITATIONS = """\
Write a "Limitations and Future Work" section for a research report.

**Research query:** {query}
**Papers analyzed:** {paper_count}
**Identified research gaps:** {gaps}
**Methodological trends:** {methods}

Write 2-4 paragraphs covering:
1. Limitations of this literature review itself
2. Gaps in the current literature
3. Promising directions for future research

Return ONLY the section text in Markdown format.\
"""


# ═══════════════════════════════════════════════════════════════════════════════
# ORCHESTRATOR PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════

ORCHESTRATOR_PLAN = """\
You are a research planning assistant. Given a research query and parameters, \
create a structured research plan.

**Research query:** {query}
**Depth:** {depth}
**Available sources:** {sources}

Generate a research plan in JSON format:
{{
    "sub_questions": [
        "3-6 specific sub-questions that break down the main query",
        "Each should be searchable as an academic query"
    ],
    "estimated_papers": {estimated_papers},
    "search_strategy": "Brief description of how to approach the search",
    "key_databases": ["Which databases to prioritize and why"]
}}

Sub-questions should be:
- Specific and searchable (not too broad)
- Cover different facets of the main question
- Complementary (not redundant)

Return ONLY the JSON object.\
"""


def format_analysis_prompt(paper: dict[str, Any]) -> tuple[str, str]:
    """Format the analysis prompt for a single paper."""
    authors = ", ".join(paper.get("authors", [])[:5])
    if len(paper.get("authors", [])) > 5:
        authors += " et al."

    user_prompt = ANALYSIS_EXTRACT.format(
        title=paper.get("title", "Unknown"),
        authors=authors or "Unknown",
        year=paper.get("year", "Unknown"),
        abstract=paper.get("abstract", "No abstract available."),
    )
    return ANALYSIS_SYSTEM, user_prompt


def format_synthesis_prompt(
    findings: list[dict[str, Any]], query: str
) -> tuple[str, str]:
    """Format the synthesis prompt for multiple paper analyses."""
    analyses_parts = []
    for i, f in enumerate(findings, 1):
        analyses_parts.append(
            f"### Paper {i}: {f.get('title', 'Unknown')}\n"
            f"- Authors: {', '.join(f.get('authors', [])[:3])}\n"
            f"- Year: {f.get('year', '?')}\n"
            f"- Claims: {'; '.join(f.get('claims', [])[:3])}\n"
            f"- Methods: {'; '.join(f.get('methods', [])[:2])}\n"
            f"- Key findings: {'; '.join(f.get('key_findings', [])[:3])}\n"
            f"- Topics: {', '.join(f.get('relevance_topics', [])[:5])}\n"
        )

    analyses_text = "\n".join(analyses_parts)
    user_prompt = SYNTHESIS_THEMES.format(
        count=len(findings),
        query=query,
        analyses_text=analyses_text,
    )
    return SYNTHESIS_SYSTEM, user_prompt


def format_section_prompt(
    section: dict[str, Any],
    query: str,
    findings_summary: str,
    synthesis_notes: str,
) -> tuple[str, str]:
    """Format a prompt for writing a single report section."""
    user_prompt = WRITING_SECTION.format(
        section_title=section.get("title", "Untitled"),
        query=query,
        outline=section.get("content_outline", ""),
        theme_description=section.get("theme_description", ""),
        paper_list=", ".join(section.get("findings", [])[:5]),
        findings=findings_summary,
        synthesis_notes=synthesis_notes,
    )
    return WRITING_SYSTEM, user_prompt


def format_abstract_prompt(
    query: str,
    depth: str,
    paper_count: int,
    themes: list[str],
    summary: str,
    gaps: list[str],
) -> tuple[str, str]:
    """Format a prompt for writing the abstract."""
    user_prompt = WRITING_ABSTRACT.format(
        query=query,
        depth=depth,
        paper_count=paper_count,
        themes=", ".join(themes[:5]),
        summary=summary,
        gaps="; ".join(gaps[:3]),
    )
    return WRITING_SYSTEM, user_prompt


def format_limitations_prompt(
    query: str,
    paper_count: int,
    gaps: list[str],
    methods: str,
) -> tuple[str, str]:
    """Format a prompt for writing limitations section."""
    user_prompt = WRITING_LIMITATIONS.format(
        query=query,
        paper_count=paper_count,
        gaps="\n".join(f"- {g}" for g in gaps),
        methods=methods,
    )
    return WRITING_SYSTEM, user_prompt


def format_plan_prompt(
    query: str, depth: str, sources: list[str]
) -> tuple[str, str]:
    """Format a prompt for the research planning step."""
    estimated = {"quick": 10, "standard": 20, "deep": 40}.get(depth, 20)
    user_prompt = ORCHESTRATOR_PLAN.format(
        query=query,
        depth=depth,
        sources=", ".join(sources),
        estimated_papers=estimated,
    )
    system = (
        "You are a research planning assistant. "
        "Return ONLY valid JSON. No markdown fences, no commentary."
    )
    return system, user_prompt
