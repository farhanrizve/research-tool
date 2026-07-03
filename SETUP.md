# Setup Guide — Research Tool

This document describes all the tools, packages, and dependencies required to perform AI-assisted research tasks using this repository. Run the environment check script to verify your setup:

```powershell
python scripts/check_environment.py
```

---

## Table of Contents

1. [System Requirements](#1-system-requirements)
2. [Python Environment](#2-python-environment)
3. [Node.js Environment](#3-nodejs-environment)
4. [LaTeX (MiKTeX)](#4-latex-miktex)
5. [Data Extraction Tools](#5-data-extraction-tools)
6. [Web Search & Browser Tools](#6-web-search--browser-tools)
7. [MCP Servers (Optional)](#7-mcp-servers-optional)
8. [Environment Check](#8-environment-check)
9. [Quick Start](#9-quick-start)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. System Requirements

| Requirement | Minimum    | Recommended |
| ----------- | ---------- | ----------- |
| **OS**      | Windows 10 | Windows 11  |
| **Python**  | 3.10+      | 3.11+       |
| **Node.js** | 18+        | 20 LTS      |
| **RAM**     | 8 GB       | 16 GB       |
| **Disk**    | 2 GB free  | 10 GB free  |
| **Git**     | 2.30+      | Latest      |

---

## 2. Python Environment

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Required Python Packages

| Package          | Purpose              | Research Task                |
| ---------------- | -------------------- | ---------------------------- |
| `pandas`         | Data manipulation    | CSV/XLSX analysis            |
| `numpy`          | Numerical computing  | Statistical analysis         |
| `scipy`          | Scientific computing | Hypothesis testing           |
| `matplotlib`     | Plotting             | Chart generation             |
| `seaborn`        | Statistical viz      | Publication figures          |
| `pymupdf`        | PDF processing       | Extract text/tables from PDF |
| `python-docx`    | DOCX processing      | Read/write Word documents    |
| `openpyxl`       | XLSX processing      | Read/write Excel files       |
| `pillow`         | Image processing     | Image analysis/OCR           |
| `requests`       | HTTP client          | Web scraping                 |
| `beautifulsoup4` | HTML parsing         | Web scraping                 |
| `lxml`           | XML/HTML parser      | Web scraping                 |
| `pytesseract`    | OCR                  | Extract text from images     |
| `transformers`   | ML models            | NLP tasks                    |
| `scikit-learn`   | ML toolkit           | Data analysis                |

---

## 3. Node.js Environment

Install npm dependencies:

```powershell
npm install
```

### Required npm Packages

| Package            | Purpose            | Research Task             |
| ------------------ | ------------------ | ------------------------- |
| `docx`             | Create Word docs   | Report generation         |
| `pptxgenjs`        | Create PowerPoint  | Presentation generation   |
| `markdown-it`      | Markdown rendering | MD to HTML conversion     |
| `@playwright/test` | Browser automation | Web scraping, screenshots |
| `playwright-core`  | Browser automation | Web data collection       |

---

## 4. LaTeX (MiKTeX)

LaTeX is required for compiling `.tex` files into PDF documents (thesis, papers, reports).

### Installation

1. Download MiKTeX from: <https://miktex.org/download>
2. Run the installer (recommended: install **for all users**)
3. Ensure MiKTeX bin directory is in your system PATH:
    - Typically: `C:\Program Files\MiKTeX\miktex\bin\x64\`
4. Verify installation:

    ```powershell
    latex --version
    pdflatex --version
    latexmk --version
    ```

### Required LaTeX Packages

Most packages will be auto-installed by MiKTeX when you first compile. Common packages:

| Package    | Purpose                      |
| ---------- | ---------------------------- |
| `geometry` | Page margins                 |
| `graphicx` | Image inclusion              |
| `natbib`   | Citation management          |
| `titlesec` | Chapter/section formatting   |
| `tocloft`  | Table of contents formatting |
| `booktabs` | Professional tables          |
| `caption`  | Figure/table captions        |
| `hyperref` | Hyperlinks                   |

### Compile Commands

```powershell
# Simple compilation
pdflatex report.tex

# Full compilation (with bibliography, cross-references)
latexmk -pdf report.tex

# Manual sequence
pdflatex report.tex
bibtex report
pdflatex report.tex
pdflatex report.tex
```

---

## 5. Data Extraction Tools

### From PDF → Text

```python
import fitz  # PyMuPDF
doc = fitz.open("document.pdf")
text = doc[0].get_text()  # First page text
```

### From PDF → Markdown

```powershell
pip install pymupdf
python -c "
import fitz
doc = fitz.open('document.pdf')
for page in doc:
    print(page.get_text())
"
```

### From DOCX → Text/Markdown

```python
from docx import Document
doc = Document("document.docx")
for para in doc.paragraphs:
    print(para.text)
```

### From CSV → Various

```python
import pandas as pd
df = pd.read_csv("data.csv")
df.to_markdown("output.md")  # Requires: pip install tabulate
```

### From XLSX → Various

```python
import pandas as pd
df = pd.read_excel("data.xlsx")
df.to_csv("output.csv")
df.to_markdown("output.md")  # Requires: pip install tabulate
```

### From Image → Text (OCR)

```python
import pytesseract
from PIL import Image
text = pytesseract.image_to_string(Image.open("figure.png"))
```

### From Web → Markdown

```python
import requests
from bs4 import BeautifulSoup
import markdownify  # pip install markdownify

r = requests.get("https://example.com")
soup = BeautifulSoup(r.text, "html.parser")
md = markdownify.markdownify(str(soup.body), heading_style="ATX")
```

---

## 6. Web Search & Browser Tools

| Tool                 | Purpose            | Setup                                            |
| -------------------- | ------------------ | ------------------------------------------------ |
| **Brave Search API** | Web search via MCP | Get API key from <https://brave.com/search/api/> |
| **Puppeteer**        | Browser automation | `npm install -g mcp-server-puppeteer`            |
| **Playwright**       | Browser automation | `npx playwright install chromium`                |

---

## 7. MCP Servers (Optional)

See `AGENTS.md` for full MCP server documentation. Quick setup:

```powershell
.\scripts\setup_env.ps1
```

---

## 8. Environment Check

Run the environment check script to verify all required tools are installed:

```powershell
python scripts/check_environment.py
```

This will check:

- Python version
- Node.js version
- Required Python packages
- Required npm packages
- LaTeX/MiKTeX installation
- Data extraction libraries
- Web search tools
- MCP server availability

---

## 9. Quick Start

```powershell
# 1. Set up Python environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Install Node dependencies
npm install

# 3. Check everything works
python scripts/check_environment.py

# 4. (Optional) Set up MCP servers
.\scripts\setup_env.ps1
```

---

## 10. Troubleshooting

### LaTeX not found

- Verify MiKTeX is installed: `latex --version`
- Check PATH: `where latex`
- Reinstall if needed from: <https://miktex.org/download>

### Python package install fails

- Upgrade pip: `pip install --upgrade pip`
- Try installing individually: `pip install <package>`
- Ensure Python 3.10+: `python --version`

### npm install fails

- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and `package-lock.json`, then retry

### Playwright browser not found

- Install Chromium: `npx playwright install chromium`
- Or: `npx playwright install --with-deps`

---

Last updated: 2026-07-04
