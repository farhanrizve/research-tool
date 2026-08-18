# AI Agents, Skills & MCP Tools for AI-Assisted Research

This document describes the AI-powered tools, skills, and MCP (Model Context Protocol) servers available in this repository to support academic research workflows.

---

## Table of Contents

1. [VS Code AI Skills](#1-vs-code-ai-skills)
2. [MCP Servers](#2-mcp-servers)
3. [Custom Agents](#3-custom-agents)
4. [Usage Workflows](#4-usage-workflows)
5. [Setup Guide](#setup-guide) <!-- markdownlint-disable-line MD051 -->

---

## 1. VS Code AI Skills

Skills are specialized instruction files that guide the AI assistant in performing specific tasks. They are located in `.agents/skills/` and are automatically loaded by VS Code's AI assistant (GitHub Copilot).

### Academic Research & Literature Skills

| Skill                       | Purpose                                               | Trigger Keywords                                                                                   |
| --------------------------- | ----------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **academic-researcher**     | Literature reviews, paper analysis, scholarly writing | "review paper", "literature review", "research paper", "methodology", "citation"                   |
| **analyze**                 | Data analysis — from quick lookups to full analyses   | "analyze data", "trend", "statistical", "metric", "report"                                         |
| **deep-research**           | Multi-source research with citation tracking          | "deep research", "comprehensive analysis", "research report", "compare X vs Y", "state of the art" |
| **tavily-research**         | AI-powered research with citations via web            | "research", "investigate", "market analysis", "detailed report"                                    |
| **thesis-workflow**         | Automated thesis/project document generation          | "thesis", "project", "proposal", "presentation", "topic work"                                      |
| **user-research**           | Plan, conduct, and synthesize user research           | "user research plan", "interview guide", "usability test", "survey design"                         |
| **data-storytelling**       | Craft compelling narratives from research data        | "data story", "data narrative", "present findings", "data visualization"                           |
| **data-quality-frameworks** | Data quality validation for research datasets         | "validate data", "data quality", "data integrity", "data contracts"                                |

### NLP, AI & Machine Learning Skills

| Skill                           | Purpose                                        | Trigger Keywords                                                      |
| ------------------------------- | ---------------------------------------------- | --------------------------------------------------------------------- |
| **ml-pipeline-workflow**        | End-to-end ML pipeline design and MLOps        | "ML pipeline", "training pipeline", "MLOps", "model deployment"       |
| **rag-implementation**          | Retrieval-Augmented Generation for AI research | "RAG", "retrieval augmented", "knowledge base", "document Q&A"        |
| **langchain-architecture**      | LangChain patterns for AI applications         | "LangChain", "AI agent", "LLM chain", "AI workflow"                   |
| **vector-index-tuning**         | Optimize vector search indexes                 | "vector search", "index tuning", "embedding index", "ANN"             |
| **embedding-strategies**        | Text embedding strategies for AI systems       | "embedding", "text embedding", "sentence embedding"                   |
| **similarity-search-patterns**  | Semantic similarity search implementation      | "similarity search", "semantic search", "nearest neighbor"            |
| **prompt-engineering-patterns** | Advanced prompt engineering techniques         | "prompt engineering", "chain-of-thought", "few-shot", "prompt design" |

### Python Development Skills

| Skill                               | Purpose                                      | Trigger Keywords                                             |
| ----------------------------------- | -------------------------------------------- | ------------------------------------------------------------ |
| **python-project-structure**        | Module architecture and project organization | "project structure", "module layout", "package organization" |
| **python-code-style**               | Python coding standards and conventions      | "code style", "PEP 8", "code format", "conventions"          |
| **python-anti-patterns**            | Common Python mistakes to avoid              | "anti-pattern", "code smell", "bad practice"                 |
| **python-design-patterns**          | Classic design patterns in Python            | "design pattern", "singleton", "factory", "observer"         |
| **python-error-handling**           | Robust error handling in Python              | "error handling", "exception", "try except", "robust"        |
| **python-testing-patterns**         | Testing strategies for Python research code  | "unit test", "testing", "pytest", "test coverage"            |
| **python-type-safety**              | Type hints and static type checking          | "type hint", "type safety", "mypy", "pyright"                |
| **python-performance-optimization** | Optimize Python code performance             | "performance", "optimization", "speed up", "profiling"       |
| **python-observability**            | Logging, monitoring, and tracing in Python   | "logging", "monitoring", "observability", "tracing"          |
| **python-configuration**            | Configuration management patterns            | "config", "settings", "environment", "dotenv"                |
| **python-resource-management**      | Resource management and context managers     | "context manager", "resource", "with statement", "cleanup"   |
| **python-packaging**                | Package creation and distribution            | "package", "PyPI", "setup.py", "distribution"                |
| **uv-package-manager**              | Fast Python dependency management with uv    | "uv", "package manager", "dependency", "venv"                |

### Document & Publishing Skills

| Skill                     | Purpose                                     | Trigger Keywords                                                                       |
| ------------------------- | ------------------------------------------- | -------------------------------------------------------------------------------------- |
| **latex-paper-en**        | English LaTeX academic paper assistant      | "compile LaTeX", "proofread paper", "fix bibliography", "three-line table", "booktabs" |
| **latex-thesis-zh**       | Chinese LaTeX thesis assistant              | Chinese degree thesis, GB/T 7714, "毕业论文", "学位论文"                               |
| **research-paper-writer** | Formal academic research papers (IEEE/ACM)  | "write research paper", "academic paper", "conference paper"                           |
| **docx**                  | Create, read, edit Word documents (.docx)   | "Word doc", "word document", ".docx"                                                   |
| **pptx**                  | Create, read, edit PowerPoint presentations | "slide deck", "presentation", ".pptx"                                                  |
| **pdf**                   | Read, merge, split, OCR PDF files           | ".pdf", "merge PDF", "extract PDF", "OCR PDF"                                          |
| **xlsx**                  | Create, edit, clean spreadsheet files       | "spreadsheet", ".xlsx", ".csv", "excel"                                                |

### Writing & Style Skills

| Skill                         | Purpose                                                           | Trigger Keywords                                            |
| ----------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------- |
| **humanize-academic-writing** | Transform AI-generated academic text to natural scholarly writing | "humanize text", "academic writing quality", "AI detection" |
| **humanizer**                 | Remove signs of AI-generated writing                              | "make more natural", "AI writing", "humanize"               |
| **web-search**                | Web search with snippets and filters                              | "search web", "find information", "look up"                 |

### Development & Workflow Skills

| Skill                            | Purpose                                           | Trigger Keywords                                      |
| -------------------------------- | ------------------------------------------------- | ----------------------------------------------------- |
| **git-advanced-workflows**       | Advanced Git workflows for research collaboration | "git workflow", "branch strategy", "merge", "rebase"  |
| **systematic-debugging**         | Structured approach to debugging code             | "debug", "bug fix", "troubleshoot", "error diagnosis" |
| **test-driven-development**      | TDD practices for reliable research code          | "TDD", "test first", "red green refactor"             |
| **task-coordination-strategies** | Coordinate multi-step research tasks              | "task coordination", "parallel work", "orchestration" |
| **mcp-builder**                  | Build custom MCP servers for research tools       | "MCP server", "MCP tool", "custom MCP"                |
| **secrets-management**           | Securely manage API keys and credentials          | "API key", "secret", "credential", "token management" |
| **bash-defensive-patterns**      | Robust shell scripting for research automation    | "bash script", "shell script", "automation"           |
| **browser-use**                  | Browser automation for web research               | "browser automation", "web scraping", "playwright"    |
| **fastapi-templates**            | FastAPI for serving research models/APIs          | "FastAPI", "API", "REST", "model serving"             |
| **image-processing**             | Image processing for research figures             | "image processing", "OCR", "image analysis"           |

### Persona Skills

| Skill                  | Purpose                                                     |
| ---------------------- | ----------------------------------------------------------- |
| **persona-researcher** | Organize research — manage references, notes, collaboration |

---

## 2. MCP Servers

MCP (Model Context Protocol) servers extend the AI assistant's capabilities with external tools. Configuration lives in `.vscode/mcp.json` — a local file (gitignored) you create per machine, so it is not tracked in the repo.

### Pre-configured MCP Servers

| Server                  | Description                                                     | How to Enable                                   |
| ----------------------- | --------------------------------------------------------------- | ----------------------------------------------- |
| **filesystem**          | File system access for reading/writing workspace files          | Pre-configured — no setup needed                |
| **sequential-thinking** | Structured step-by-step reasoning for complex research problems | Pre-configured — no setup needed                |
| **puppeteer**           | Browser automation for web scraping and data collection         | Requires: `npm install -g mcp-server-puppeteer` |
| **brave-search**        | Web search via Brave Search API                                 | Requires: Brave Search API key in env           |
| **multi-mcp**           | Multi-model code review (GPT, Claude, Gemini)                   | Requires: clone repo + API keys (see below)     |
| **blind-auditor**       | Self-auditing code review system                                | Requires: clone repo + rules config (see below) |

### Installing Optional MCP Servers

#### Multi-MCP (Multi-Model Code Review)

```powershell
# Clone into .mcp-servers/
cd .mcp-servers
git clone https://github.com/religa/multi_mcp.git
cd multi_mcp
uv sync
cp .env.example .env
# Edit .env with your API keys (at least one of: OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY)
```

**Usage:** "multi codereview [file]" — analyzes code with multiple AI models in parallel.

#### Blind-Auditor (Code Auditing)

```powershell
cd .mcp-servers
git clone https://github.com/Sim-xia/Blind-Auditor.git
cd Blind-Auditor
uv sync
# Edit rules.json with your project's code standards
```

**Usage:** Forces AI to self-audit generated code before outputting.

---

## 3. Custom Agents

This repository contains reusable AI agent configuration files that can be used across different AI coding tools (GitHub Copilot, Claude Code, Cursor, etc.).

### Agent Configuration Files

| File                    | Purpose                                                        |
| ----------------------- | -------------------------------------------------------------- |
| `.vscode/mcp.json`      | MCP server configuration for VS Code _(local, not tracked)_    |
| `.vscode/settings.json` | VS Code settings optimized for research _(local, not tracked)_ |
| AGENTS.md (this file)   | Agent documentation and usage guide                            |

### Agent Workflows

#### Research Paper Review

1. Use **academic-researcher** skill to analyze papers
2. Use **pdf** skill to extract paper content
3. Use **thesis-workflow** to track papers and update thesis
4. Use **humanize-academic-writing** to polish writing

#### Data Analysis

1. Use **analyze** skill to structure the analysis
2. Use **xlsx** skill for spreadsheet operations
3. Use **scripts/validate_csv.py** for data validation
4. Use **puppeteer** MCP for web data collection

#### Thesis Writing

1. Use **latex-paper-en** or **latex-thesis-zh** for LaTeX compilation
2. Use **research-paper-writer** for drafting
3. Use **deep-research** for literature review
4. Use **tavily-research** for comprehensive citation-backed research

---

## 4. Usage Workflows

### Quick Start: New Research Project

```markdown
1. Start with: "Start new thesis with topic: [YOUR TOPIC]"
   → Triggers thesis-workflow skill
2. Add research papers: "Analyze paper: [PATH/URL]"
   → Triggers pdf + academic-researcher skills
3. Review literature: "Deep research on [TOPIC]"
   → Triggers deep-research skill
4. Draft proposal: "Write proposal for [TOPIC]"
   → Triggers research-paper-writer skill
5. Polish writing: "Humanize this text"
   → Triggers humanize-academic-writing skill
```

### Quality Assurance for Research Code

````markdown
1. "Review this analysis code" → Uses multi-mcp if configured
2. "Validate this CSV data" → Uses scripts/validate_csv.py
3. "Clean this dataset" → Uses scripts/clean_csv.py
4. "Generate schema diagram" → Uses scripts/generate_schema_diagram.py

---

<a name="setup-guide"></a>

## Setup Guide

### First-Time Setup

```powershell
# 1. Install Python virtual environment (uses uv — fast, no pip needed)
uv venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install the package (editable) with all extras
uv pip install -e ".[all]"

# 3. (Optional) Install Node dependencies
npm install

# 4. (Optional) Install MCP server dependencies
.\scripts\setup_env.ps1
```
````

### Requirements

- **Python 3.10+** — for data analysis scripts
- **Node.js 18+** — for document generation (docx, pptx) and MCP servers
- **VS Code** — with GitHub Copilot extension for AI assistance
- **LaTeX distribution** (optional) — for thesis compilation (MiKTeX or TeX Live)

---

Last updated: 2026-07-04
