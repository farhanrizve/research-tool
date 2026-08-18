---
name: research-pipeline
description: |
  Orchestrate the full research workflow from query to report.
  Use when: running a research query end-to-end, conducting automated literature review,
  executing the research pipeline, or when user says "research", "run research",
  "literature review", "conduct research", "full research pipeline".
license: MIT
metadata:
  author: research-tool
  version: "1.0.0"
---

# Research Pipeline

Orchestrates the complete research workflow: Query → Plan → Discover → Analyze → Synthesize → Write.

## When to Use

- User wants to run a full research pipeline on a topic
- Conducting an automated literature review
- Searching for papers and generating a synthesis report
- User says "research X", "literature review on Y", "find papers about Z"

## Pipeline Stages

```
1. PLAN       → Break query into sub-questions, estimate paper count
2. DISCOVER   → Search Semantic Scholar, arXiv, web in parallel
3. INDEX      → Store papers in knowledge base (ChromaDB)
4. ANALYZE    → Extract claims, methods, findings via LLM
5. SYNTHESIZE → Identify themes, contradictions, research gaps
6. WRITE      → Generate structured report with citations
```

## CLI Usage

```bash
# Quick research (10 papers, 3 sub-questions)
research run "What are the latest advances in federated learning?" --depth quick

# Standard research (25 papers, 5 sub-questions)
research run "Impact of transformer architectures on NLP" --depth standard

# Deep research (50 papers, 8 sub-questions)
research run "Comprehensive survey of RAG techniques" --depth deep

# Specify sources
research run "LLM alignment methods" --sources arxiv,semantic_scholar

# Resume a paused session
research session resume <session-id>
```

## MCP Server Usage

```python
# Via MCP tool call
research_conduct(
    query="What are the latest advances in federated learning?",
    depth="standard",
    sources=["arxiv", "semantic_scholar"],
    human_checkpoint=True
)
```

## Human Checkpoints

The pipeline pauses at key decision points (unless `--auto-approve` is set):

1. **Plan Approval** — Review sub-questions before search begins
2. **Synthesis Review** — Approve themes and findings before report generation

## Configuration

| Setting | Env Variable | Default |
|---------|-------------|---------|
| LLM Model | `RESEARCH_LLM_MODEL` | `gpt-4o-mini` |
| Default Depth | `RESEARCH_DEFAULT_DEPTH` | `standard` |
| Auto-approve | `RESEARCH_AUTO_APPROVE` | `false` |
| Max Concurrent | `RESEARCH_MAX_CONCURRENT_AGENTS` | `5` |

## Output

Reports are saved to the project directory as:
- `report.md` — Markdown format (default)
- `report.tex` — LaTeX format (with `--format latex`)
- `session.json` — Session state for resume
