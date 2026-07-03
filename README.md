# Research Tool — AI-Assisted Academic Research Suite

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Node.js 18+](https://img.shields.io/badge/Node.js-18%2B-green)](https://nodejs.org)
[![VS Code](https://img.shields.io/badge/VS%20Code-Copilot-007ACC)](https://code.visualstudio.com)
[![LaTeX](https://img.shields.io/badge/LaTeX-XeLaTeX-008080)](https://miktex.org)

An AI-powered research assistant workspace with **48 specialized skills**, reusable LaTeX templates, data processing scripts, and automated research workflows — all designed to accelerate academic research from literature review to final publication.

Powered by [VS Code](https://code.visualstudio.com) + [GitHub Copilot](https://github.com/features/copilot) + [MCP](https://modelcontextprotocol.io) tools.

---

## ✨ Features

- **🧠 48 AI Research Skills** — Auto-loaded by Copilot for literature review, paper analysis, LaTeX compilation, PDF/data extraction, academic writing, and more
- **📄 LaTeX Thesis Templates** — Full `book`-class thesis structure with front-matter, 6 chapters, per-chapter variables, and XeLaTeX compilation
- **📊 Data Processing Scripts** — CSV validation, cleaning, schema diagram generation, and environment checks
- **📚 Literature Management** — Organized folders for reading lists, paper summaries, comparison matrices, and critical notes
- **🔬 Data Extraction** — Structured storage for extracted tables, figures, quotes, and data points from papers
- **📝 Document Generation** — Skills and templates for Word (`.docx`), PowerPoint (`.pptx`), PDF, and spreadsheets (`.xlsx`)
- **🌐 Web Research Tools** — MCP servers for web search, browser automation, and paper fetching
- **🔧 MCP Server Support** — Optional multi-model code review (GPT + Claude + Gemini) and self-auditing review

---

## 🚀 Quick Start

```powershell
# 1. Clone or open this repo in VS Code

# 2. Activate Python virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Install Node.js dependencies
npm install

# 4. Verify everything is ready
python scripts/check_environment.py
```

> **First time?** Start with [`AGENTS.md`](AGENTS.md) for the full skill catalog, then read [`RESEARCH_WORKFLOW.md`](RESEARCH_WORKFLOW.md) for guided workflows.

---

## 📂 Project Structure

```text
research-tool/
├── AGENTS.md                 ← Full skill/MCP/agent catalog
├── SETUP.md                  ← Installation & dependency guide
├── RESEARCH_WORKFLOW.md      ← AI agent execution workflows
│
├── .agents/skills/           ← 48 AI skills (auto-loaded)
├── scripts/                  ← Automation & data processing
├── templates/                ← LaTeX thesis, guidelines, patterns
├── reports/                  ← Reusable LaTeX report templates
├── literatures/              ← Reading lists, summaries, matrices
├── extractions/              ← Extracted tables, figures, quotes
├── data/                     ← Datasets, outputs, notebooks
├── papers/                   ← Downloaded & reviewed papers
├── thesis/                   ← Thesis LaTeX source
└── docs/                     ← Proposals, reports, meeting notes
```

---

## 🧠 Key Skills at a Glance

| Category               | Skills                                                                      |
| ---------------------- | --------------------------------------------------------------------------- |
| **Literature Review**  | `academic-researcher`, `deep-research`, `tavily-research`                   |
| **Paper Analysis**     | `pdf`, `docx`, `xlsx`, `mcp_web-reader-se_webReader`                        |
| **LaTeX / Thesis**     | `latex-paper-en`, `latex-thesis-zh`, `research-paper-writer`                |
| **Data Analysis**      | `analyze`, `data-storytelling`, `data-quality-frameworks`                   |
| **Writing & Polish**   | `humanize-academic-writing`, `humanizer`                                    |
| **Web / Browser**      | `web-search`, `browser-use`                                                 |
| **Python Development** | 13 skills covering structure, style, testing, packaging, performance        |
| **AI / ML**            | `rag-implementation`, `ml-pipeline-workflow`, `prompt-engineering-patterns` |
| **MCP Servers**        | `multi-mcp`, `blind-auditor`, `puppeteer`, `brave-search`                   |

See [`AGENTS.md`](AGENTS.md) for the complete catalog with trigger keywords.

---

## 📖 Documentation

| Document                                               | Purpose                                                  |
| ------------------------------------------------------ | -------------------------------------------------------- |
| [`AGENTS.md`](AGENTS.md)                               | Full catalog of AI skills, MCP servers, and agents       |
| [`SETUP.md`](SETUP.md)                                 | Detailed installation and dependency guide               |
| [`RESEARCH_WORKFLOW.md`](RESEARCH_WORKFLOW.md)         | Workflow guides, storage conventions, and best practices |
| [`templates/latex-guide.md`](templates/latex-guide.md) | Comprehensive LaTeX reference                            |
| [`templates/thesis-book/`](templates/thesis-book/)     | Full thesis book template (6 chapters)                   |

---

## 🤖 How It Works

This repository is designed for **VS Code + GitHub Copilot**. When you describe a task in natural language, Copilot automatically activates the relevant skill from `.agents/skills/` to guide the AI assistant:

> _"Review this paper PDF"_ → activates `pdf` + `academic-researcher` skills
>
> _"Compile my thesis"_ → activates `latex-paper-en` skill
>
> _"Analyze this CSV dataset"_ → activates `analyze` + `xlsx` skills
>
> _"Humanize this chapter"_ → activates `humanize-academic-writing` skill

No commands to remember — just describe what you need.

---

## 🔧 Optional MCP Servers

| Server            | Purpose                                     | Setup                                 |
| ----------------- | ------------------------------------------- | ------------------------------------- |
| **puppeteer**     | Browser automation & web scraping           | `npm install -g mcp-server-puppeteer` |
| **brave-search**  | Web search via Brave API                    | Requires API key                      |
| **multi-mcp**     | Multi-model code review (GPT+Claude+Gemini) | Clone to `.mcp-servers/`              |
| **blind-auditor** | Self-auditing code review                   | Clone to `.mcp-servers/`              |

---

## 🛠 Requirements

- **VS Code** with [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) extension
- **Python 3.10+** — for data analysis and automation scripts
- **Node.js 18+** — for document generation and MCP servers
- **LaTeX** (MiKTeX or TeX Live) — for thesis compilation (optional)

---

## 📬 License & Author

**Author:** [Md. Farhan Tanvir Rizve](https://github.com/farhanrizve)  
**Repository:** [github.com/farhanrizve/research-tool](https://github.com/farhanrizve/research-tool)
