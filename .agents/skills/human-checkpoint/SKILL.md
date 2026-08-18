---
name: human-checkpoint
description: |
  Interactive approval gates for the research pipeline — human-in-the-loop control.
  Use when: pausing for human approval, reviewing research plans, approving synthesis,
  checking intermediate results, or when user says "pause for review", "approve plan",
  "review findings", "human checkpoint", "approval gate".
license: MIT
metadata:
  author: research-tool
  version: "1.0.0"
---

# Human Checkpoint

Manages interactive approval gates throughout the research pipeline.

## When to Use

- Pausing the pipeline for human review at key decision points
- Presenting research plans for approval before execution
- Reviewing synthesis results before report generation
- Allowing manual source selection or prioritization
- Verifying extracted claims against source material

## Checkpoint Types

| Checkpoint | When | What's Shown |
|-----------|------|-------------|
| `plan_approval` | Before search begins | Sub-questions, sources, estimated paper count |
| `source_selection` | After initial search | Found papers, allow filtering/prioritization |
| `claim_verification` | After analysis | Extracted claims vs source text |
| `review_synthesis` | Before writing | Themes, gaps, contradictions, section outline |
| `draft_review` | After writing | Generated report sections |
| `citation_check` | Before export | Bibliography completeness |
| `final_approval` | Before export | Full report summary |

## CLI Behavior

With human checkpoints (default):
```
📋 Research Plan
  Query: What are the latest advances in federated learning?
  Sub-questions: 5
  Sources: semantic_scholar, arxiv, web
  Estimated papers: ~25

Proceed with this research plan? [Y/n]:
```

With auto-approve (`--auto-approve` or `RESEARCH_AUTO_APPROVE=true`):
```
  [orchestrator] Auto-approving plan — skipping checkpoint
```

## Configuration

| Setting | Env Variable | Default | Description |
|---------|-------------|---------|-------------|
| Auto-approve | `RESEARCH_AUTO_APPROVE` | `false` | Skip all checkpoints |
| Timeout | `RESEARCH_CHECKPOINT_TIMEOUT` | `300` | Seconds to wait for input |

## MCP Usage

When used as an MCP server, checkpoints can be:
- **Enabled** — Server returns to the caller for approval
- **Disabled** — Full autonomous execution
- **Callback-based** — Caller provides approval webhook

```python
# Autonomous mode (no checkpoints)
research_conduct(query="...", human_checkpoint=False)

# Interactive mode (pauses for approval)
research_conduct(query="...", human_checkpoint=True)
```

## Best Practices

1. **Always review the plan** — Ensure sub-questions are relevant and non-redundant
2. **Check synthesis themes** — Verify they match your understanding of the field
3. **Spot-check citations** — Confirm key papers are included
4. **Use auto-approve cautiously** — Only for well-defined, repetitive queries
