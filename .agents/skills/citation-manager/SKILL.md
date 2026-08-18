---
name: citation-manager
description: |
  Manage citations — BibTeX, formatting, verification, and bibliography generation.
  Use when: adding citations, formatting references, generating bibliography,
  verifying citation accuracy, converting citation styles, or when user mentions
  "citation", "bibliography", "BibTeX", "reference list", "cite sources".
license: MIT
metadata:
  author: research-tool
  version: "1.0.0"
---

# Citation Manager

Manages the full citation lifecycle: capture → format → verify → export.

## When to Use

- Adding papers to a citation database
- Formatting citations in APA, MLA, Chicago, IEEE, or GB/T 7714
- Generating a bibliography from collected references
- Verifying that citations in a document match the database
- Converting between citation styles

## CLI Usage

```bash
# Add a BibTeX file to the database
research cite add references.bib

# Add a single paper by DOI
research cite add-doi 10.1234/example.5678

# Format all citations in a document
research cite format --style apa --input draft.md

# Verify citations in a document
research cite check --document report.md

# Export bibliography
research cite export --style ieee --output bibliography.bib

# List all citations in database
research cite list --format bibtex
```

## Citation Styles

| Style | Command | Common Use |
|-------|---------|------------|
| APA 7th | `--style apa` | Psychology, Social Sciences |
| MLA 9th | `--style mla` | Humanities, Literature |
| Chicago | `--style chicago` | History, Arts |
| IEEE | `--style ieee` | Engineering, CS |
| GB/T 7714 | `--style gbt7714` | Chinese academic papers |
| Vancouver | `--style vancouver` | Medicine, Biology |

## BibTeX Format

```bibtex
@article{author2024title,
  author  = {Author, A. and Author, B.},
  title   = {Paper Title},
  journal = {Journal Name},
  year    = {2024},
  volume  = {10},
  number  = {2},
  pages   = {100--120},
  doi     = {10.1234/example.5678},
}
```

## Verification Checks

When verifying citations, check:
1. **Completeness** — All cited papers have bibliographic data
2. **Accuracy** — Author names, years, and titles match
3. **Consistency** — Same citation style used throughout
4. **Currency** — No outdated references when recent work exists
5. **Quality** — Sources are peer-reviewed when possible

## Integration with Pipeline

The citation manager integrates with the research pipeline:
- Papers found during `DISCOVER` are auto-indexed with DOIs
- `ANALYZE` extracts citation-relevant metadata
- `WRITE` generates inline `[Author, Year]` citations
- Final report includes a formatted bibliography
