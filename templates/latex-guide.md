# LaTeX Writing Guide

**For thesis/report writing with LaTeX** — covers document structure, essential commands, formatting, math, tables, figures, citations, and troubleshooting.

---

## Table of Contents

1.  [What is LaTeX?](#1-what-is-latex)
2.  [Document Structure](#2-document-structure)
3.  [Document Classes](#3-document-classes)
4.  [Preamble & Packages](#4-preamble--packages)
5.  [Text Formatting](#5-text-formatting)
6.  [Sections & Headings](#6-sections--headings)
7.  [Lists](#7-lists)
8.  [Tables](#8-tables)
9.  [Figures & Images](#9-figures--images)
10. [Mathematics](#10-mathematics)
11. [Citations & Bibliography](#11-citations--bibliography)
12. [Multi-File Projects](#12-multi-file-projects)
13. [Cross-Referencing](#13-cross-referencing)
14. [Appendices](#14-appendices)
15. [Special Characters](#15-special-characters)
16. [Page Breaks](#16-page-breaks)
17. [Hyperlinks & PDF Settings](#17-hyperlinks--pdf-settings)
18. [Page Layout & Margins](#18-page-layout--margins)
19. [Common Packages](#19-common-packages)
20. [Cheat Sheet](#20-cheat-sheet)
21. [Troubleshooting](#21-troubleshooting)
22. [Tools & Editors](#22-tools--editors)

---

## 1. What is LaTeX?

LaTeX is a document preparation system for high-quality typesetting. It is the standard for academic papers, theses, and technical documents.

**Key ideas:**
- You write plain text with markup commands
- LaTeX handles formatting, layout, and typography automatically
- Content is separated from presentation
- Output is PDF

**Basic workflow:**

```
.tex source → LaTeX compiler → .pdf output
                 ↑
        .bib bibliography file
```

Compile sequence for documents with bibliography, table of contents, and cross-references:

```bash
pdflatex document.tex
bibtex document          # only if you have citations
pdflatex document.tex    # resolve references
pdflatex document.tex    # final pass (until labels settle)
```

---

## 2. Document Structure

Every LaTeX document has two parts: **preamble** and **body**.

### Skeleton

```latex
\documentclass[12pt,a4paper]{report}

% --- Preamble ---
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\geometry{left=1in,right=1in,top=1in,bottom=1in}
\usepackage{graphicx}
\graphicspath{{images/}}
\usepackage{setspace}
\onehalfspacing

\begin{document}

% --- Front matter ---
\frontmatter
\maketitle
\tableofcontents
\listoffigures
\listoftables

% --- Main content ---
\mainmatter
\chapter{Introduction}
...
\chapter{Conclusion}

% --- Back matter ---
\bibliographystyle{apalike}
\bibliography{references}

\end{document}
```

### Front matter vs Main matter vs Back matter

| Section | Commands | Page numbering | Chapter numbering |
|---------|----------|----------------|-------------------|
| Front matter | `\frontmatter` | Roman (i, ii, iii) | Unnumbered |
| Main matter | `\mainmatter` | Arabic (1, 2, 3) | Numbered |
| Back matter | `\backmatter` | Arabic (continues) | Unnumbered |

Note: `\frontmatter`, `\mainmatter`, `\backmatter` are **only** available in `book` class and its derivatives (like this thesis's `report` class with manual equivalents).

---

## 3. Document Classes

```latex
\documentclass[options]{class}
```

| Class | Use case | Key features |
|-------|----------|--------------|
| `article` | Journal papers, essays, short reports | No chapters; title on first page |
| `report` | Theses, long reports, project books | Has `\chapter`; separate title page |
| `book` | Books, dissertations | Front/back matter; two-sided by default |
| `beamer` | Presentations/slides | Frame-based slides |
| `letter` | Formal correspondence | Predefined sender/recipient fields |
| `standalone` | Single diagrams or tikz pictures | Crops to content |

### Common options

| Option | Effect |
|--------|--------|
| `10pt`, `11pt`, `12pt` | Font size (default: 10pt) |
| `a4paper`, `letterpaper` | Paper size |
| `oneside`, `twoside` | Single or double-sided |
| `onecolumn`, `twocolumn` | Single or two-column layout |
| `openright`, `openany` | Chapters start on right/any page |
| `landscape` | Landscape orientation |
| `draft` | Shows overfull boxes as black bars |

---

## 4. Preamble & Packages

The preamble is everything between `\documentclass` and `\begin{document}`.

### Loading packages

```latex
\usepackage{package-name}
\usepackage[options]{package-name}
\usepackage{package1,package2,package3}
```

### Custom commands

```latex
\newcommand{\name}[num-args]{definition}
\renewcommand{\name}[num-args]{definition}  % redefine existing
\providecommand{\name}[num-args]{definition} % only if not defined

% Examples
\newcommand{\R}{\mathbb{R}}
\newcommand{\todo}[1]{\textcolor{red}{[TODO: #1]}}
```

### Defining variables (constants)

Use `\def` to define reusable numeric/text constants — centralize them so you only change values in one place.

**Pattern used in this thesis (Chapter 0–6 with `variables_*.tex`):**

```
report/
  Chapter 1/
    chapter_1.tex       % \input{variables_1} at top
    variables_1.tex     % all \def statements here
  Chapter 2/
    chapter_2.tex
    variables_2.tex
  ...
```

**variables_1.tex:**

```latex
\def\sampleSize{4000}
\def\significanceLevel{0.05}
\def\surveyYear{2025}
\def\confidenceInterval{95}
```

**chapter_1.tex:**

```latex
\chapter{Introduction}

\input{variables_1}

We surveyed \sampleSize\ respondents at a \confidenceInterval\% confidence level.
```

**Why use `\def` instead of `\newcommand`?**

| Command | Behavior |
|---------|----------|
| `\def\name{val}` | Overwrites silently — use intentionally for variables you control |
| `\newcommand{\name}{val}` | Errors if already defined — safer but inflexible for multi-file scope |
| `\renewcommand{\name}{val}` | Only works if already defined |
| `\providecommand{\name}{val}` | Defines only if not already defined |

**Naming conventions:**

- Use camelCase or PascalCase: `\def\sampleSize{100}` instead of `\def\samplesize{100}`
- Prefix with chapter: `\def\chOneSampleSize{100}`
- Keep all `\def` statements in `variables_*.tex` files, one per chapter
- Load variables at the top of each chapter file with `\input{variables_N}`

**Use cases for variables:**

- Sample sizes, population counts, threshold values
- Statistical constants (confidence levels, effect sizes)
- Version numbers, dates
- Figure/table counts
- Any number or string that appears more than once

---

## 5. Text Formatting

| Command | Output |
|---------|--------|
| `\textbf{bold}` | **bold** |
| `\textit{italic}` | *italic* |
| `\underline{under}` | underline |
| `\texttt{mono}` | `monospace` |
| `\textsc{Small Caps}` | Small Caps |
| `\emph{emphasize}` | *emphasize* (context-aware) |
| `\textsf{sans}` | sans-serif |
| `\textsl{slanted}` | slanted |

### Font sizes

```latex
{\tiny tiny}
{\scriptsize scriptsize}
{\footnotesize footnotesize}
{\small small}
{\normalsize normalsize}  (default)
{\large large}
{\Large Large}
{\LARGE LARGE}
{\huge huge}
{\Huge Huge}
```

### Paragraph formatting

```latex
\setlength{\parindent}{0pt}   % no indent
\setlength{\parskip}{0pt}     % no space between paragraphs
\setlength{\parskip}{6pt}     % 6pt space between paragraphs
```

### Line spacing

```latex
\usepackage{setspace}
\singlespacing
\onehalfspacing      % 1.5 line spacing (recommended for theses)
\doublespacing
```

---

## 6. Sections & Headings

### Sectioning commands

```latex
\part{Part Title}
\chapter{Chapter Title}       % only in report, book
\section{Section Title}
\subsection{Subsection Title}
\subsubsection{Sub-subsection}
\paragraph{Paragraph}
\subparagraph{Subparagraph}
```

### Unnumbered versions (add `*`)

```latex
\section*{Introduction}
\chapter*{Abstract}
```

**Note:** Unnumbered sections don't appear in the table of contents by default. To add them:

```latex
\chapter*{Abstract}
\addcontentsline{toc}{chapter}{Abstract}
```

### Section numbering depth

```latex
\setcounter{tocdepth}{3}       % appears in TOC: section, subsection, subsubsection
\setcounter{secnumdepth}{3}    % numbered: section, subsection, subsubsection
```

Levels: `-1` = part, `0` = chapter, `1` = section, `2` = subsection, `3` = subsubsection, `4` = paragraph

---

## 7. Lists

### Bullet list (itemize)

```latex
\begin{itemize}
  \item First item
  \item Second item
  \item Third item
\end{itemize}
```

### Numbered list (enumerate)

```latex
\begin{enumerate}
  \item First
  \item Second
  \item Third
\end{enumerate}
```

### Description list

```latex
\begin{description}
  \item[Term] Definition
  \item[Another] Explanation
\end{description}
```

### Customizing lists (enumitem package)

```latex
\usepackage{enumitem}

% No spacing between items
\begin{itemize}[noitemsep]

% Custom label
\begin{enumerate}[label=(\roman*)]

% Horizontal spacing
\begin{itemize}[leftmargin=1cm]
```

---

## 8. Tables

### Simple table (tabular)

```latex
\begin{tabular}{|l|c|r|}
  \hline
  Left & Center & Right \\
  \hline
  1 & 2 & 3 \\
  4 & 5 & 6 \\
  \hline
\end{tabular}
```

Column specifiers: `l` = left, `c` = center, `r` = right, `p{width}` = paragraph column, `|` = vertical line

### Professional table (booktabs)

```latex
\usepackage{booktabs}

\begin{table}[h]
  \centering
  \caption{Skill Demand Rankings}
  \label{tab:skills}
  \begin{tabular}{lcc}
    \toprule
    Skill & Frequency & Percentage \\
    \midrule
    Python     & 450 & 72.1\% \\
    SQL        & 400 & 64.0\% \\
    JavaScript & 350 & 56.0\% \\
    \bottomrule
  \end{tabular}
\end{table}
```

Placement specifiers: `h` = here, `t` = top of page, `b` = bottom, `p` = separate float page, `!` = override defaults

### Multi-page table

```latex
\usepackage{longtable}

\begin{longtable}{lcc}
  \caption{Long table caption}
  \label{tab:long} \\
  \toprule
  Header 1 & Header 2 & Header 3 \\
  \midrule
  \endfirsthead
  \multicolumn{3}{c}{Continued from previous page} \\
  \toprule
  Header 1 & Header 2 & Header 3 \\
  \midrule
  \endhead
  \bottomrule
  \endfoot
  Data 1 & Data 2 & Data 3 \\
  ...
\end{longtable}
```

---

## 9. Figures & Images

### Single image

```latex
\usepackage{graphicx}
\graphicspath{{images/}}  % where images are stored

\begin{figure}[h]
  \centering
  \includegraphics[width=0.8\textwidth]{filename}
  \caption{Descriptive caption}
  \label{fig:my-label}
\end{figure}
```

### Size options for includegraphics

| Option | Example | Effect |
|--------|---------|--------|
| `width=` | `width=0.5\textwidth` | Scale to fraction of text width |
| `height=` | `height=5cm` | Fixed height |
| `scale=` | `scale=0.75` | Scale factor |
| `angle=` | `angle=90` | Rotate degrees |

### Multiple images side by side

```latex
\usepackage{subcaption}

\begin{figure}[h]
  \centering
  \begin{subfigure}{0.45\textwidth}
    \includegraphics[width=\textwidth]{fig1}
    \caption{First}
    \label{fig:first}
  \end{subfigure}
  \hfill
  \begin{subfigure}{0.45\textwidth}
    \includegraphics[width=\textwidth]{fig2}
    \caption{Second}
    \label{fig:second}
  \end{subfigure}
  \caption{Combined figure}
  \label{fig:combined}
\end{figure}
```

---

## 10. Mathematics

### Modes

| Syntax | Mode |
|--------|------|
| `$x^2 + y^2 = z^2$` | Inline math |
| `\[ x^2 + y^2 = z^2 \]` | Display math (numbered with `\begin{equation}`) |
| `\begin{equation} ... \end{equation}` | Numbered equation |
| `\begin{align} ... \end{align}` | Multi-line aligned equations |

### Common math commands

| Command | Result |
|---------|--------|
| `x^{2}` | x² |
| `x_{i}` | xᵢ |
| `\frac{a}{b}` | a/b |
| `\sqrt{x}` | √x |
| `\sqrt[n]{x}` | ⁿ√x |
| `\sum_{i=1}^{n}` | Σᵢ₌₁ⁿ |
| `\int_{a}^{b}` | ∫ₐᵇ |
| `\lim_{x \to \infty}` | limₓ→∞ |
| `\alpha, \beta, \gamma` | α, β, γ |
| `\times, \div, \pm` | ×, ÷, ± |
| `\leq, \geq, \neq, \approx` | ≤, ≥, ≠, ≈ |
| `\infty, \partial, \nabla` | ∞, ∂, ∇ |
| `\rightarrow, \Rightarrow` | →, ⇒ |
| `\in, \notin, \subset` | ∈, ∉, ⊂ |
| `\forall, \exists` | ∀, ∃ |
| `\mathbf{x}` | **x** (bold) |
| `\mathrm{text}` | roman text in math |
| `\text{words}` | text inside math |

### Equation alignment

```latex
\begin{align}
  y &= mx + b \label{eq:line} \\
  E &= mc^{2} \label{eq:einstein}
\end{align}
```

---

## 11. Citations & Bibliography

### Bibliography file (.bib)

```bibtex
@article{key2024,
  author  = {Author, First},
  title   = {Paper Title},
  journal = {Journal Name},
  year    = {2024},
  volume  = {10},
  pages   = {1--10}
}

@book{key2023,
  author    = {Writer, Sam},
  title     = {Book Title},
  publisher = {Publisher},
  year      = {2023}
}

@inproceedings{key2022,
  author    = {Researcher, A.},
  title     = {Conference Paper},
  booktitle = {Proceedings},
  year      = {2022}
}

@online{key2025,
  author  = {Organization},
  title   = {Web Page Title},
  year    = {2025},
  url     = {https://example.com}
}
```

### Citation commands (natbib)

| Command | Output style |
|---------|-------------|
| `\cite{key}` | (Author, Year) |
| `\citep{key}` | (Author, Year) — parenthetical |
| `\citet{key}` | Author (Year) — textual |
| `\cite{key1,key2}` | (Author1, Year1; Author2, Year2) |
| `\cite[chap. 2]{key}` | (Author, Year, chap. 2) |
| `\cite[see][p. 5]{key}` | (see Author, Year, p. 5) |
| `\nocite{*}` | Include all bib entries (even uncited) |

### Bibliography styles

```latex
\bibliographystyle{apalike}    % APA-like (alphabetical)
\bibliographystyle{plain}      % numbered, alphabetical
\bibliographystyle{ieeetr}     % numbered, order of appearance
\bibliographystyle{agsm}       % Harvard style
\bibliographystyle{acm}        % ACM style
```

### Bibliography in document

```latex
\bibliographystyle{apalike}
\bibliography{references}     % references.bib (no extension)
```

---

## 12. Multi-File Projects

### `\input` vs `\include` vs `\includeonly`

| Command | Behavior | Best for |
|---------|----------|----------|
| `\input{file}` | Inserts file contents directly (like copy-paste) | Small files, variables, preamble chunks |
| `\include{file}` | Starts new page, adds `.aux` for cross-refs | Chapter-level files in large documents |
| `\includeonly{file1,file2}` | Only compiles listed `\include` files (saves time) | During editing — comment out finished chapters |

**Rules:**
- `\include` cannot be nested inside each other
- `\input` can be nested anywhere
- Always use `.tex` extension in `\input`, never in `\include`

**Recommended thesis pattern:**

```latex
% report.tex
\includeonly{Chapter 1/chapter_1, Chapter 3/chapter_3}  % only compile these

\mainmatter
\include{Chapter 1/chapter_1}
\include{Chapter 2/chapter_2}
\include{Chapter 3/chapter_3}
...
```

### Using `\includeonly` for faster compilation

```latex
% Only compile chapters 1 and 3 (skip 2, 4, 5, 6)
\includeonly{Chapter 1/chapter_1, Chapter 3/chapter_3}

% All \include lines stay — ignored ones keep existing .aux for cross-refs
\include{Chapter 1/chapter_1}
\include{Chapter 2/chapter_2}    % skipped — uses old .aux
\include{Chapter 3/chapter_3}
\include{Chapter 4/chapter_4}    % skipped
```

**Note for Overleaf:** Works the same way — just put `\includeonly{...}` in the main file.

---

## 13. Cross-Referencing

### Labels and references

```latex
\section{Results}
\label{sec:results}

As shown in Section~\ref{sec:results} — use ~ for non-breaking space
See Figure~\ref{fig:chart}
Table~\ref{tab:data} presents...
Equation~\eqref{eq:model}
```

### `\phantomsection`

When adding something to the TOC manually (like unnumbered sections), use `\phantomsection` so hyperlinks point to the right page:

```latex
\clearpage
\phantomsection
\addcontentsline{toc}{chapter}{List of Figures}
\listoffigures
```

---

## 14. Appendices

Use `\appendix` to switch from chapters to appendices:

```latex
\appendix
\chapter{Survey Questionnaire}
\chapter{Additional Tables}
\chapter{Interview Protocol}
```

After `\appendix`:
- Numbering changes from "Chapter 1" to "Appendix A"
- Sections become "A.1", "A.2", etc.
- Page numbering continues from main matter

With `\include`:

```latex
\appendix
\include{Chapter A/appendix_a}
\include{Chapter B/appendix_b}
```

---

## 15. Special Characters

In LaTeX, these characters have special meaning and must be escaped:

| Character | Command | Purpose |
|-----------|---------|---------|
| `%` | `\%` | Comment |
| `$` | `\$` | Math mode |
| `#` | `\#` | Parameter |
| `&` | `\&` | Column separator |
| `_` | `\_` | Subscript |
| `{` | `\{` | Group begin |
| `}` | `\}` | Group end |
| `~` | `\textasciitilde{}` | Non-breaking space |
| `^` | `\textasciicircum{}` | Superscript |
| `\` | `\textbackslash{}` | Command prefix |

**Percent sign example:**

```latex
The unemployment rate dropped by 5\% this year.
We surveyed 85\% of employers.
```

**Ampersand in company names:**

```latex
AT\&T announced new policies.  % renders as "AT&T"
```

**Tilde in URLs (use `\url` instead):**

```latex
\usepackage{url}
\url{https://example.com/~user}  % handles ~ automatically
```

---

## 16. Page Breaks

| Command | Effect |
|---------|--------|
| `\newpage` | Start new page; doesn't flush pending figures/tables |
| `\clearpage` | Start new page AND flush all pending floats |
| `\cleardoublepage` | Start next right-hand (odd) page; insert blank if needed |

**Usage:**

```latex
\clearpage          % before important sections
\cleardoublepage    % before chapters in two-sided documents
```

For `\cleardoublepage` with `hyperref`, add `\phantomsection` before it:

```latex
\cleardoublepage
\phantomsection
\chapter{Introduction}
```

---

## 17. Hyperlinks & PDF Settings

The `hyperref` package generates clickable links and PDF bookmarks.

### Basic usage

```latex
\usepackage[
  colorlinks=true,
  linkcolor=black,
  citecolor=black,
  urlcolor=blue,
  pdfauthor={Your Name},
  pdftitle={Thesis Title},
  pdfsubject={Thesis},
  pdfkeywords={LaTeX, thesis, skills}
]{hyperref}
```

### Important options

| Option | Values | Effect |
|--------|--------|--------|
| `colorlinks` | `true`, `false` | Colored text vs colored boxes |
| `linkcolor` | color name | Color for internal links (TOC, refs) |
| `citecolor` | color name | Color for citation links |
| `urlcolor` | color name | Color for URL links |
| `bookmarks` | `true`, `false` | Generate PDF bookmarks |
| `bookmarksnumbered` | `true`, `false` | Include section numbers in bookmarks |
| `pdfpagemode` | `FullScreen`, `UseOutlines` | How PDF reader opens |

### Best practice for thesis submission

Use black links (no colored text in printed copy):

```latex
\usepackage[colorlinks=true, linkcolor=black, citecolor=black, urlcolor=blue]{hyperref}
```

**Always load `hyperref` LAST** — after all other packages.

---

| Prefix | For |
|--------|-----|
| `sec:` | Sections |
| `fig:` | Figures |
| `tab:` | Tables |
| `eq:` | Equations |
| `ch:` | Chapters |
| `app:` | Appendices |

---

## 18. Page Layout & Margins

### Using geometry package

```latex
\usepackage{geometry}

% Simple margins
\geometry{margin=1in}

% Specific margins (tmargin=top, bmargin=bottom, lmargin=left, rmargin=right)
\geometry{a4paper, tmargin=1in, rmargin=0.8in, bmargin=1in, lmargin=1.2in}

% With binding offset
\geometry{bindingoffset=0.5cm}
```

### Headers and footers

```latex
\usepackage{fancyhdr}

\pagestyle{fancy}
\fancyhf{}                    % clear all
\fancyhead[L]{\leftmark}      % chapter name on left
\fancyhead[R]{\thepage}       % page number on right
\fancyfoot[C]{\thepage}       % page number centered in footer
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}
```

---

## 19. Common Packages

| Package | Purpose |
|---------|---------|
| `amsmath` | Advanced math environments |
| `amssymb` | Math symbols |
| `graphicx` | Image inclusion |
| `geometry` | Page margins |
| `setspace` | Line spacing |
| `natbib` | Citation management |
| `booktabs` | Professional tables |
| `longtable` | Multi-page tables |
| `tabularx` | Tables with auto-width columns |
| `float` | Better float placement |
| `caption` | Custom caption formatting |
| `subcaption` | Sub-figures/sub-tables |
| `hyperref` | Hyperlinks and PDF bookmarks |
| `url` | URL formatting with line breaks |
| `enumitem` | Custom list formatting |
| `titlesec` | Custom section heading styles |
| `tocloft` | Custom table of contents |
| `fancyhdr` | Custom headers/footers |
| `tikz` | Diagrams and drawings |
| `pgfplots` | Graphs and charts |
| `rotating` | Rotated tables/figures |
| `multicol` | Multi-column layouts |
| `xcolor` | Colors |
| `listings` | Source code listings |
| `minted` | Syntax-highlighted code |
| `glossaries` | Glossary and acronyms |
| `lipsum` | Lorem ipsum filler text |
| `blindtext` | Blind text for testing |

---

## 20. Cheat Sheet

### Essential commands quick reference

```
Document structure
  \documentclass[12pt,a4paper]{report}
  \usepackage{package}
  \begin{document} ... \end{document}
  \frontmatter \mainmatter \backmatter

Sectioning
  \part{} \chapter{} \section{} \subsection{} \subsubsection{}

Text formatting
  \textbf{} \textit{} \underline{} \texttt{} \emph{} \textsc{}

Lists
  \begin{itemize} \item ... \end{itemize}
  \begin{enumerate} \item ... \end{enumerate}
  \begin{description} \item[term] ... \end{description}

Tables
  \begin{tabular}{lcr} ... \end{tabular}
  \begin{table}[h] \caption{} \label{} \end{table}

Figures
  \includegraphics[width=0.5\textwidth]{file}
  \begin{figure}[h] \centering \caption{} \label{} \end{figure}

Citations
  \cite{key} \citep{key} \citet{key}
  \bibliographystyle{apalike} \bibliography{file}

Math
  $...$ (inline) \[...\] (display)
  \begin{equation} \label{} ... \end{equation}
  \begin{align} ... \end{align}
  ^{superscript} _{subscript}
  \frac{}{} \sqrt{} \sum_{}^{} \int_{}^{}

Cross-referencing
  \label{sec:name} \ref{sec:name} \pageref{sec:name}

Page layout
  \newpage \clearpage \cleardoublepage
  \thispagestyle{empty}
  \setlength{\parindent}{0pt}
  \setlength{\parskip}{0pt}
```

---

## 21. Troubleshooting

### Common errors

| Error | Likely cause | Fix |
|-------|-------------|-----|
| `! Undefined control sequence` | Command doesn't exist | Check spelling, load package |
| `! LaTeX Error: File ... not found` | Missing file | Check path and filename |
| `! Package natbib Error: Bibliography not compatible` | BibTeX/Biber mismatch | Use correct bibliography processor |
| `! Missing $ inserted` | Math command outside math mode | Add `$...$` or `\[...\]` |
| `Overfull \hbox` | Text too wide for page | Reword, use `\sloppy`, or `\hyphenation{}` |
| `Underfull \hbox` | Poor line break | Usually harmless |
| `Label(s) may have changed. Rerun` | Cross-references out of sync | Rerun pdflatex |
| `Citation(s) may have changed. Rerun` | Bib refs out of sync | Run bibtex + 2× pdflatex |
| `! LaTeX Error: Too many unprocessed floats` | Too many figures/tables | Add `[h]` or `[H]`, or use `\clearpage` |

### Best practices

1. **Compile frequently** — catch errors early
2. **Use complete compile cycle** — `pdflatex → bibtex → pdflatex → pdflatex`
3. **Keep a clean `.tex` structure** — one file per chapter
4. **Use `variables_*.tex` files** — centralize numeric constants
5. **Version control** — use Git (LaTeX source files are plain text)
6. **Avoid manual numbering** — use `\label`/`\ref`
7. **Don't fight LaTeX's spacing** — let it handle justification
8. **Use `\phantomsection`** before adding items to TOC manually
9. **Test on Overleaf** — catches missing packages early
10. **Read `.log` files** — they tell you exactly what went wrong

### If compilation fails

```bash
# Quick check — find actual errors
grep "^!" report.log

# Count errors
grep -c "^!" report.log

# See all warnings
grep "Warning" report.log
```

---

## 22. Tools & Editors

### Online editors (recommended for collaboration)

| Tool | URL | Notes |
|------|-----|-------|
| Overleaf | https://www.overleaf.com | Most popular; real-time collaboration; template gallery |
| Underleaf | https://www.underleaf.ai | AI-assisted LaTeX; good for beginners |

### Local editors

| Tool | Platform | Notes |
|------|----------|-------|
| TeXworks | Cross-platform | Simple; bundled with MiKTeX |
| TeXstudio | Cross-platform | Feature-rich IDE |
| Visual Studio Code + LaTeX Workshop | Cross-platform | Free; powerful; git integration |
| WinEdt | Windows | Popular in academic settings |

### LaTeX distributions

| Distribution | Platform | Notes |
|-------------|----------|-------|
| MiKTeX | Windows | Current project uses this |
| TeX Live | Cross-platform | Most comprehensive |
| MacTeX | macOS | TeX Live for Mac |

### Reference resources

| Resource | URL |
|----------|-----|
| Overleaf Learn | https://www.overleaf.com/learn |
| LaTeX Wikibook | https://en.wikibooks.org/wiki/LaTeX |
| CTAN (packages) | https://ctan.org |
| TeX Stack Exchange | https://tex.stackexchange.com |
| Detexify (symbol lookup) | https://detexify.kirelabs.org |
| LaTeX cheat sheet (PDF) | https://tug.ctan.org/info/latex-refsheet/LaTeX_RefSheet.pdf |

---

*Generated for the thesis project at `report/`. For this project specifically, compile with `pdflatex report.tex && bibtex report && pdflatex report.tex && pdflatex report.tex` from the `report/` directory.*
