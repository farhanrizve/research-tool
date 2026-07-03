# Reports — Reusable LaTeX Report Templates

This directory contains a complete, reusable LaTeX report template structure based on the thesis patterns found in [`e:\github\thesis`](../e:\github\thesis). It provides a consistent chapter structure with per-chapter variables, shared formatting, and front-matter templates that can be adapted for any research topic.

## Directory Structure

```text
reports/
├── report.tex                       # Main document — compiles everything
├── shared/                          # Shared configuration
│   ├── packages.tex                 #   LaTeX packages (natbib, geometry, etc.)
│   ├── formatting.tex               #   Layout, fonts, spacing, captions
│   ├── report-variables.tex         #   Global metadata (title, author, etc.)
│   ├── abbreviations.tex            #   Abbreviations list template
│   └── references.bib               #   Bibliography placeholder
├── front-matter/                    # Document preliminaries
│   ├── title-page.tex               #   Title page
│   ├── abstract.tex                 #   Abstract (~300 words)
│   ├── acknowledgements.tex         #   Acknowledgements
│   ├── declaration.tex              #   Declaration of originality
│   ├── certificate.tex              #   Supervisor's certificate
│   └── transmittal.tex              #   Letter of transmittal
├── chapters/                        # Chapter templates (6 chapters)
│   ├── 01-introduction/             #   Chapter 1: Introduction
│   │   ├── chapter.tex              #     Content template with TODO guides
│   │   └── variables.tex            #     Per-chapter \def macros
│   ├── 02-literature-review/        #   Chapter 2: Literature Review
│   ├── 03-methodology/              #   Chapter 3: Methodology
│   ├── 04-results/                  #   Chapter 4: Results
│   ├── 05-discussion/               #   Chapter 5: Discussion
│   └── 06-conclusion/               #   Chapter 6: Conclusion
└── images/                          # Place figures here
    └── .gitkeep
```

## Key Features

- **Per-chapter variables** — Each chapter has a `variables.tex` with `\def` macros for numeric constants (sample sizes, thresholds, metrics). Reference them in text as `\variableName`.
- **Global report variables** — `shared/report-variables.tex` defines `\ReportTitle`, `\ReportAuthor`, `\ReportSupervisor`, etc., used across front-matter files.
- **Consistent formatting** — `shared/packages.tex` loads all packages; `shared/formatting.tex` configures fonts, spacing, headings, and floats.
- **TODO-guided templates** — Every `chapter.tex` contains commented `% TODO` markers showing exactly what to write in each section.
- **Topic-agnostic** — Rename chapters, add/remove sections. The structure works for any research domain.

## How to Use

### Quick Start

1. **Set global metadata** — Edit `shared/report-variables.tex`:

    ```latex
    \def\ReportTitle{Your Research Title}
    \def\ReportAuthor{Your Name}
    \def\ReportSupervisor{Supervisor Name}
    % ... etc.
    ```

2. **Write your chapters** — For each chapter in `chapters/`:
    - Edit `variables.tex` to define topic-specific constants
    - Edit `chapter.tex` replacing `% TODO` sections with your content

3. **Add references** — Edit `shared/references.bib` with your bibliography entries. Cite with `\citep{key}` or `\citet{key}`.

4. **Add figures** — Place `.png`, `.jpg`, or `.pdf` files in `images/` and include with:

    ```latex
    \includegraphics[width=\textwidth]{images/your-figure.png}
    ```

5. **Edit front matter** — Update the files in `front-matter/` (abstract, acknowledgements, etc.) for your project.

6. **Compile** — Use `xelatex` (recommended) or `latexmk`:

    ```bash
    # With latexmk (automatic):
    latexmk -xelatex report.tex

    # Manual sequence:
    xelatex report.tex
    bibtex report
    xelatex report.tex
    xelatex report.tex
    ```

### Customizing the Structure

- **Add a new chapter** — Create `chapters/07-new-topic/chapter.tex` and `variables.tex`, then add `\input{chapters/07-new-topic/chapter}` to `report.tex`.
- **Remove a chapter** — Comment out or delete the corresponding `\input{}` line in `report.tex`.
- **Change chapter order** — Reorder the `\input{}` lines in `report.tex`.

### Per-Chapter Variable Pattern

The per-chapter `variables.tex` files use `\def` to define reusable constants. Example from the thesis repo:

```latex
% chapters/01-introduction/variables.tex
\def\gradCount{20000}
\def\placementRate{77.1}
\def\unemployedCount{906000}
```

Reference them in `chapter.tex` as `\gradCount`, `\placementRate`, etc. This keeps all numeric values in one place for easy updating.

## Requirements

### Compilation

- **XeLaTeX** (recommended) — handles Unicode and custom fonts
- **BibTeX** — for bibliography compilation
- LaTeX distribution: [MiKTeX](https://miktex.org/) (Windows), [TeX Live](https://tug.org/texlive/) (Linux/Mac), or [MacTeX](https://tug.org/mactex/) (Mac)

### Packages (auto-loaded via `shared/packages.tex`)

The template uses standard LaTeX packages: `natbib`, `geometry`, `graphicx`, `fontspec`, `amsmath`, `titlesec`, `tocloft`, `booktabs`, `longtable`, `hyperref`, `caption`, `fancyhdr`, and others.

## Origin

This template was extracted and generalized from the thesis structure at `e:\github\thesis\thesis\report\`, which follows the `book` document class layout with:

- `Chapter N/chapter_N.tex` — chapter content
- `Chapter N/variables_N.tex` — per-chapter definitions
- `Chapter X/packages.tex` / `formatting.tex` — shared configuration
- `Chapter 0/` — front-matter files
- `Chapter7/references.bib` — bibliography

---

Last updated: 2026-07-04
