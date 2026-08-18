---
name: research-project
description: |
  Research project lifecycle management — create, track, resume, and export projects.
  Use when: starting a new research project, checking project status, resuming research,
  managing multiple research projects, exporting results, or when user says
  "new research project", "check progress", "resume research", "project status",
  "list projects", "export report".
license: MIT
metadata:
  author: research-tool
  version: "1.0.0"
---

# Research Project Manager

Manages the full lifecycle of research projects — from initialization to export.

## When to Use

- Starting a new research project with a topic
- Checking the status of ongoing research
- Resuming a paused or interrupted research session
- Listing all research projects
- Exporting final reports in different formats
- Managing multiple concurrent research projects

## CLI Usage

```bash
# Initialize a new research project
research init "AI in Healthcare" --dir ./my-project

# List all research projects
research project list

# Check project status
research project status <project-id>

# Resume a paused session
research session resume <session-id>

# List all sessions
research session list

# Export report in different formats
research project export <project-id> --format pdf
research project export <project-id> --format docx
research project export <project-id> --format latex
```

## Project Structure

```
research-project/
├── session.json          # Session state (status, plan, findings)
├── report.md             # Generated report (Markdown)
├── report.tex            # Generated report (LaTeX, optional)
├── references.bib        # Bibliography file
├── papers/               # Indexed papers metadata
│   ├── paper-001.json
│   └── paper-002.json
├── extractions/          # Paper analysis results
│   ├── analysis-001.json
│   └── synthesis.json
└── .env                  # Project-specific config overrides
```

## Session Persistence

Research sessions are saved to `session.json` and can be resumed:

```json
{
  "id": "abc123",
  "query": "What are the latest advances in federated learning?",
  "status": "analyzing",
  "depth": "standard",
  "sources": ["semantic_scholar", "arxiv"],
  "plan": { "sub_questions": [...], "estimated_papers": 25 },
  "findings": [...],
  "checkpoints": [...],
  "created_at": "2026-08-18T10:00:00Z",
  "updated_at": "2026-08-18T10:05:00Z"
}
```

## Project Status Values

| Status | Meaning |
|--------|---------|
| `created` | Project initialized, not yet started |
| `planning` | Generating research plan |
| `discovering` | Searching for papers |
| `analyzing` | Extracting claims and findings |
| `synthesizing` | Combining findings into themes |
| `writing` | Generating report |
| `done` | Research complete |
| `failed` | Pipeline failed (see error) |

## Multi-Project Management

```bash
# List all projects with status
research project list

# Output:
# ID        Query                              Status    Papers  Last Updated
# abc123    Federated learning advances        done      24      2026-08-18
# def456    Transformer architectures for NLP  analyzing 12      2026-08-18
# ghi789    RAG techniques survey              writing   48      2026-08-17
```

## Export Formats

| Format | Command | Notes |
|--------|---------|-------|
| Markdown | `--format markdown` | Default, includes inline citations |
| LaTeX | `--format latex` | For academic submission |
| PDF | `--format pdf` | Requires LaTeX distribution |
| DOCX | `--format docx` | Via Node.js docx library |
| PPTX | `--format pptx` | Presentation slides |
