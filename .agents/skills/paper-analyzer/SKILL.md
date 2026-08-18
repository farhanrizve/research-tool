---
name: paper-analyzer
description: |
  Extract structured information from research papers — claims, methods, findings, contributions.
  Use when: analyzing a research paper, extracting key information from papers,
  reviewing paper methodology, assessing evidence quality, or when user says
  "analyze paper", "extract claims", "review methodology", "assess this paper".
license: MIT
metadata:
  author: research-tool
  version: "1.0.0"
---

# Paper Analyzer

Extracts structured information from research papers using LLM-powered analysis with heuristic fallback.

## When to Use

- Analyzing a single paper for claims, methods, and findings
- Batch-analyzing multiple papers from search results
- Assessing evidence quality of research
- Extracting methodology details for comparison
- Building a structured overview of a paper's contributions

## Extraction Schema

Each paper analysis produces:

```json
{
  "title": "Paper Title",
  "authors": ["Author A", "Author B"],
  "year": 2024,
  "claims": ["Claim 1", "Claim 2"],
  "methods": ["Method 1", "Method 2"],
  "key_findings": ["Finding 1", "Finding 2"],
  "contributions": ["Contribution 1"],
  "limitations": ["Limitation 1"],
  "evidence_quality": "high|medium|low",
  "evidence_reasoning": "Why this quality rating",
  "relevance_topics": ["topic1", "topic2"],
  "_llm_powered": true
}
```

## CLI Usage

```bash
# Analyze a single paper (PDF)
research extract paper.pdf --tables --figures --claims

# Batch analyze papers in a directory
research extract batch ./papers/ --output ./extractions/

# Analyze from URL
research lit analyze --url https://arxiv.org/abs/2401.12345
```

## LLM Analysis Prompts

The analyzer uses structured prompts that request:

1. **Claims** — What do the authors assert? (1-5 items)
2. **Methods** — What techniques/approaches are used? (1-3 items)
3. **Key Findings** — What results are reported? (1-5 items)
4. **Contributions** — What is novel? (1-3 items)
5. **Limitations** — What is missing or acknowledged as weak? (0-3 items)
6. **Evidence Quality** — high/medium/low with reasoning

## Heuristic Fallback

When LLM is unavailable, extraction falls back to keyword-based heuristics:

- **Claims**: Sentences containing "we show", "we find", "results show"
- **Methods**: Sentences containing "using", "via", "approach", "framework"
- **Findings**: Sentences containing "achieve", "outperform", "significant"
- **Quality**: Based on citation count (>100 = high, >20 = medium, else low)

## Evidence Quality Tiers

| Tier | Criteria | Example |
|------|----------|---------|
| **High** | Large-scale RCT, meta-analysis, >100 citations | Cochrane review |
| **Medium** | Controlled study, >20 citations, peer-reviewed | Conference paper |
| **Low** | Preliminary, <20 citations, preprint | Workshop paper |

## Batch Processing

For analyzing multiple papers concurrently:
- Concurrency bounded by `RESEARCH_MAX_CONCURRENT_AGENTS` (default: 5)
- Failed analyses fall back to heuristic extraction
- Results cached for 1 hour to avoid redundant LLM calls
