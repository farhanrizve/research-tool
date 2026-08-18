---
name: environment-awareness
description: |
    Environment awareness skill — detects the current system, available MCP servers,
    agent plugins, installed runtimes, and tool capabilities. Use when: the user asks
    "what tools do I have?", "what MCP servers are available?", "check my environment",
    "what can you do?", "what extensions are loaded?", or when a task requires knowing
    what external tools/APIs/capabilities are reachable.
license: MIT
metadata:
    author: research-tool
    version: "1.0.0"
---

# Environment Awareness

You are an environment-aware assistant. Before performing complex tasks, assess what
tools, runtimes, MCP servers, and agent plugins are available in the current workspace.

---

## When to Apply

Use this skill when:

- User asks "what tools do you have?" or "what can you access?"
- User asks about MCP servers, agent plugins, or extensions
- A task requires an external tool (browser, database, file system, API) and you need
  to verify it's available before attempting to use it
- Debugging why a tool call failed ("is this MCP server running?")
- Onboarding a new user to the workspace
- Starting a session and need to inventory capabilities

---

## Detection Procedure

Run these checks **in order**. Each section builds on the previous one.

### Step 1 — System & Runtime Inventory

Detect the host machine and available runtimes:

```powershell
# OS & machine
[System.Environment]::OSVersion
$env:COMPUTERNAME

# Runtimes
python --version           # Python
node --version             # Node.js
uv --version               # uv package manager
dotnet --version           # .NET
java -version 2>&1         # Java
go version                 # Go
rustc --version            # Rust

# Shell
$PSVersionTable.PSVersion.ToString()
```

Record which runtimes are **present** and which are **absent**.

### Step 2 — Workspace Project Type

Detect what kind of project this is:

```powershell
# Check for project markers
if (Test-Path package.json)    { "Node.js project" }
if (Test-Path pyproject.toml)  { "Python project" }
if (Test-Path Cargo.toml)      { "Rust project" }
if (Test-Path go.mod)          { "Go project" }
if (Test-Path *.sln)           { ".NET solution" }
if (Test-Path Dockerfile)      { "Docker containerized" }
if (Test-Path .env)            { "Has .env config" }
if (Test-Path .env.example)    { "Has .env.example template" }
```

### Step 3 — MCP Server Discovery

MCP (Model Context Protocol) servers extend the AI assistant with external tools.
Check for MCP configuration in these locations (in priority order):

| Location                    | Scope                            |
| --------------------------- | -------------------------------- |
| `.vscode/mcp.json`          | Workspace — VS Code MCP config   |
| `~/.config/mcp/config.json` | User — global MCP config         |
| `mcp.json` (project root)   | Project — standalone MCP config  |
| `.mcp/` directory           | Project — MCP server definitions |

Read any found MCP config files and extract:

- **Server names** and their transport types (`stdio`, `sse`, `streamable-http`)
- **Command** or **URL** for each server
- **Environment variables** each server needs

For each MCP server, determine its **status**:

- `stdio` servers: check if the command binary exists (`Get-Command <cmd>`)
- `sse`/`http` servers: check if the URL is reachable (`Invoke-WebRequest -Uri <url> -Method HEAD`)

### Step 4 — Agent Plugin Discovery

Agent plugins are installed as VS Code extensions or MCP servers that provide
domain-specific tools. Check:

```
# VS Code extensions (agent plugins)
code --list-extensions 2>$null

# Known MCP-based agent plugins (look for these names):
# - playwright           → browser automation
# - context7             → library documentation lookup
# - firecrawl            → web crawling & research
# - figma                → design-to-code
# - github               → GitHub PR/issue management
# - notion               → Notion workspace integration
# - vercel               → deployment & hosting
# - hugging-face         → ML models & datasets
# - chrome-devtools      → browser DevTools interaction
# - tavily               → web search & extraction
```

### Step 5 — Available Tool Categories

Based on detected MCP servers and extensions, classify available tools into categories:

| Category          | Key Tools                                                                    | When to Use                           |
| ----------------- | ---------------------------------------------------------------------------- | ------------------------------------- |
| **File System**   | `read_file`, `write_file`, `grep_search`, `list_dir`                         | Always available — workspace access   |
| **Browser/Web**   | `open_browser_page`, `click_element`, `navigate_page`, `run_playwright_code` | UI testing, screenshots, web scraping |
| **Terminal**      | `run_in_terminal`, `get_terminal_output`                                     | Build, run, install, debug            |
| **Search**        | `vscode-websearchforcopilot_webSearch`, `mcp_tavily_*`                       | Up-to-date web information            |
| **GitHub**        | `mcp_github_*`                                                               | PRs, issues, code search              |
| **Figma**         | `mcp_figma_*`                                                                | Design work, component mapping        |
| **Documentation** | `mcp_microsoft_*`, `mcp_context7_*`                                          | Library/API docs lookup               |
| **Web Crawling**  | `mcp_firecrawl_*`, `mcp_tavily_*`                                            | Multi-page research, site mapping     |
| **Database**      | `dbclient_*`                                                                 | SQL queries, schema inspection        |
| **Notebook**      | `run_notebook_cell`, `create_new_jupyter_notebook`                           | Data analysis, exploration            |
| **Memory**        | `memory` (create/view/str_replace)                                           | Cross-session notes                   |

---

## Report Format

When the user asks about their environment, present findings in this structure:

```markdown
## 🖥️ System

- **OS:** Windows 10.0.x / macOS / Linux
- **Machine:** HOSTNAME
- **Shell:** PowerShell 7.x / bash / zsh

## ⚡ Runtimes

| Runtime | Version | Status           |
| ------- | ------- | ---------------- |
| Python  | 3.14.6  | ✅ EnvKit        |
| Node.js | 26.7.0  | ✅               |
| uv      | 0.12.5  | ✅               |
| Go      | —       | ❌ Not installed |

## 🔌 MCP Servers

| Server     | Transport | Status         | Tools Provided         |
| ---------- | --------- | -------------- | ---------------------- |
| filesystem | stdio     | ✅ Running     | read, write, search    |
| tavily     | stdio     | ✅ Running     | search, crawl, extract |
| playwright | stdio     | ⚠️ Not started | browser automation     |

## 🧩 Agent Plugins

| Plugin                     | Status | Capabilities                     |
| -------------------------- | ------ | -------------------------------- |
| github.vscode-pull-request | ✅     | PR review, issue management      |
| figma.mcp-server           | ✅     | Design-to-code, Figma read/write |

## 📦 Workspace

- **Project type:** Python (pyproject.toml)
- **Config:** .env ✅, .env.example ✅
- **Venv:** .venv/ ✅

## 🔧 Quick Reference

- **Search web:** use `vscode-websearchforcopilot_webSearch`
- **Browser test:** activate web interaction tools, then use playwright
- **GitHub:** activate github tools, then use mcp_github_* tools
```

---

## Capability Gating Rules

1. **Never assume a tool is available.** Always check before calling.
2. **MCP servers may be configured but not running.** For `stdio` servers, they
   start on first use. For `http`/`sse` servers, verify reachability.
3. **Some tools require activation first.** Groups like `activate_web_interaction_tools`
   must be called before their child tools become callable.
4. **Rate limits apply.** Free-tier APIs (Zen, Semantic Scholar, Tavily) have
   throttling. Stagger requests and use retry logic.
5. **Sensitive keys live in `.env`.** Never echo API keys. Reference them by
   env var name only.

---

## Quick Diagnostics

If a tool call fails, run this diagnostic:

```powershell
# 1. Is the MCP server process alive?
Get-Process | Where-Object { $_.ProcessName -match "mcp|node|python" }

# 2. Is the env var set?
$env:RESEARCH_ZEN_API_KEY   # Check Zen
$env:RESEARCH_TAVILY_API_KEY  # Check Tavily

# 3. Is the Python venv activated?
.venv\Scripts\python.exe --version

# 4. Are dependencies installed?
.venv\Scripts\pip.exe list | Select-String "litellm|chromadb|httpx"
```

---

## Auto-Invocation

This skill should be **automatically triggered** at the start of any complex
multi-tool workflow to ensure the required capabilities are present before
committing to an execution plan. If a required tool is missing, inform the user
and suggest alternatives.
