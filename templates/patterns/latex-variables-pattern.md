# LaTeX Variables Pattern

**Purpose:** Centralize reusable constants per chapter using `\def` commands to avoid hardcoding numbers and strings throughout your thesis.
**Origin:** Adapted from the LaTeX Writing Guide variables pattern used in `E:\github\thesis`.

---

## Why Use This Pattern

- **Single source of truth** — change a value once, it updates everywhere
- **Per-chapter scoping** — each chapter has its own `variables_N.tex` file
- **Clear naming** — camelCase names make values self-documenting
- **Easy maintenance** — no more searching through 100+ pages of LaTeX to find a hardcoded number

---

## File Structure

```text
├── Chapter 1/
│   ├── chapter_1.tex
│   └── variables_1.tex      ← all \def statements for Chapter 1
├── Chapter 2/
│   ├── chapter_2.tex
│   └── variables_2.tex      ← all \def statements for Chapter 2
├── Chapter 3/
│   ├── chapter_3.tex
│   └── variables_3.tex
...
```

### In each `variables_N.tex` file

```latex
% ── Chapter 1: Introduction ────────────────────────────────────────────
\def\sampleSize{4000}
\def\significanceLevel{0.05}
\def\surveyYear{2025}
\def\confidenceInterval{95}
\def\populationEstimate{20000}
\def\responseRate{38}
\def\surveyMonths{6}
```

### In each `chapter_N.tex` file

```latex
\chapter{Introduction}

\input{variables_1}

We surveyed \sampleSize\ respondents at a \confidenceInterval\% confidence level.
The survey was conducted over \surveyMonths\ months in \surveyYear.
```

### Compile sequence (when using per-chapter variables)

```bash
latexmk -pdf report.tex
# or manually:
pdflatex report.tex
bibtex report
pdflatex report.tex
pdflatex report.tex
```

---

## Command Cheat Sheet

| Command                       | Behavior                                                              | Best for                     |
| ----------------------------- | --------------------------------------------------------------------- | ---------------------------- |
| `\def\name{val}`              | Overwrites silently — use intentionally for variables you control     | Per-chapter variables        |
| `\newcommand{\name}{val}`     | Errors if already defined — safer but inflexible for multi-file scope | Global constants             |
| `\renewcommand{\name}{val}`   | Only works if already defined                                         | Overriding existing commands |
| `\providecommand{\name}{val}` | Defines only if not already defined                                   | Fallback defaults            |

## Naming Conventions

- Use **camelCase**: `\def\sampleSize{100}` not `\def\samplesize{100}`
- Prefix with chapter when needed: `\def\chOneSampleSize{100}`
- Keep **all** `\def` statements in `variables_*.tex` files, one per chapter
- Load variables at the **top** of each chapter file with `\input{variables_N}`

## What to Put in Variables

| Category                                  | Examples                                                                           |
| ----------------------------------------- | ---------------------------------------------------------------------------------- |
| **Sample sizes**                          | `\def\sampleSize{4000}`, `\def\controlGroup{200}`                                  |
| **Statistical constants**                 | `\def\confidenceLevel{95}`, `\def\significanceLevel{0.05}`, `\def\effectSize{0.3}` |
| **Dates & versions**                      | `\def\surveyYear{2025}`, `\def\thesisVersion{1.2}`                                 |
| **Counts & thresholds**                   | `\def\totalPostings{10986}`, `\def\minFrequency{3}`                                |
| **Repeated phrases**                      | `\def\institutionName{World University of Bangladesh}`                             |
| **File paths**                            | `\def\imageDir{images/}`, `\def\dataDir{../data/}`                                 |
| **Any number/string used more than once** |                                                                                    |
