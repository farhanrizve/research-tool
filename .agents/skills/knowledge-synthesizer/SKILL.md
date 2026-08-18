---
name: knowledge-synthesizer
description: |
  Combine findings from multiple papers into coherent themes, identify patterns,
  detect contradictions, and build narrative structure.
  Use when: synthesizing research findings, identifying themes across papers,
  detecting contradictions, building a literature review structure, or when
  user says "synthesize findings", "combine results", "identify themes",
  "what are the patterns", "literature synthesis".
license: MIT
metadata:
  author: research-tool
  version: "1.0.0"
---

# Knowledge Synthesizer

Combines analysis results from multiple papers into structured themes, patterns, and narrative.

## When to Use

- Synthesizing findings from multiple analyzed papers
- Identifying common themes across a literature corpus
- Detecting contradictions or debates between papers
- Building a structured outline for a literature review
- Identifying research gaps and future directions

## Synthesis Output Schema

```json
{
  "themes": [
    {
      "name": "Theme name",
      "description": "2-3 sentence description",
      "paper_titles": ["Paper A", "Paper B"],
      "consensus": "What the literature agrees on",
      "debate": "Disagreements within this theme"
    }
  ],
  "cross_cutting_insights": ["Insight spanning multiple themes"],
  "contradictions": [
    {
      "papers": ["Paper A", "Paper B"],
      "description": "What the contradiction is about"
    }
  ],
  "research_gaps": ["Gap 1", "Gap 2"],
  "methodological_trends": "Overview of methods used",
  "temporal_trends": "How the field has evolved"
}
```

## LLM Synthesis Process

1. **Format inputs** — Convert paper analyses into a structured prompt
2. **Theme identification** — LLM groups papers by major themes
3. **Pattern detection** — Identify consensus and contradictions
4. **Gap analysis** — Find under-explored areas
5. **Section generation** — Convert themes into report section outlines

## Heuristic Fallback

When LLM is unavailable, synthesis uses keyword-based grouping:

| Theme | Keywords |
|-------|----------|
| Methodology | method, approach, framework, algorithm, model |
| Performance | accuracy, performance, benchmark, evaluation |
| Challenges | challenge, limitation, problem, difficulty |
| Applications | application, use case, deployment, real-world |
| Future Work | future, direction, open problem, next step |

## Integration with Pipeline

```
DISCOVER → papers
    ↓
ANALYZE → findings (per-paper extractions)
    ↓
SYNTHESIZE → themes, gaps, contradictions, section outlines
    ↓
WRITE → structured report with LLM-written prose
```

## Contradiction Detection

The synthesizer identifies contradictions by finding papers that:
- Report opposite results on the same metric
- Use incompatible methodologies for similar questions
- Reach different conclusions from similar data
- Disagree on theoretical interpretations
