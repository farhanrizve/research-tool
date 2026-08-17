# Research Tool Upgrade Plan

> **Vision:** A fully programmable, AI-autonomous, human-in-the-loop, all-purpose research platform  
> **Architecture:** CLI + AI Agentic (Phase 1-3) → Web App (Phase 4)  
> **Date:** 2026-08-17

---

## Executive Summary

Transform the current research-tool repository from a collection of scripts and templates into a **unified, production-grade research platform** that rivals tools like GPT-Researcher (29k★), Feynman, and STORM — but with a unique focus on **human-in-the-loop control** and **extensible MCP-based tool integration**.

### Key Differentiators from Existing Tools

| Feature                       | GPT-Researcher | Feynman | STORM | **This Tool**      |
| ----------------------------- | -------------- | ------- | ----- | ------------------ |
| Multi-agent orchestration     | ✅             | ✅      | ✅    | ✅                 |
| Human-in-the-loop checkpoints | ❌             | Partial | ❌    | ✅ **Core focus**  |
| MCP tool extensibility        | ✅             | ✅      | ❌    | ✅ **First-class** |
| Local-first option            | ❌             | ✅      | ❌    | ✅                 |
| Web app ready                 | ❌             | ✅      | ❌    | ✅ **API-first**   |
| Custom skill system           | ❌             | ✅      | ❌    | ✅ **48 skills**   |
| Citation management           | ✅             | ✅      | ✅    | ✅                 |
| Multi-format export           | ✅             | ✅      | ❌    | ✅                 |

---

## Current State Analysis

### What We Have

```
research-tool/
├── .agents/skills/          # 48 AI skills (literature, NLP, ML, docs, writing)
├── extractions/             # Empty — ready for new research
├── literatures/             # Empty — ready for reading lists
├── reports/                 # LaTeX template structure (generic)
├── scripts/                 # Environment check, CSV tools
├── templates/               # Guidelines, thesis patterns
├── requirements.txt         # 182 Python packages
└── package.json             # 39 npm packages
```

### What's Missing

1. **No CLI entry point** — No `research` command, no subcommands
2. **No agent orchestration** — Skills exist but no coordinator to chain them
3. **No research pipeline** — No query → search → analyze → synthesize flow
4. **No human-in-the-loop** — No approval gates, no interactive checkpoints
5. **No MCP server** — Can't be used by other AI agents
6. **No project management** — No way to track research projects/progress
7. **No knowledge base** — No RAG, no embeddings, no vector search
8. **No API layer** — No programmatic access for future web app

---

## Architecture Design

### Core Principle: **Orchestrator → Specialists → Human**

```
┌─────────────────────────────────────────────────────────────┐
│                        USER LAYER                           │
│  CLI / Future Web UI / MCP Client                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   ORCHESTRATOR AGENT                        │
│  • Parses research intent                                   │
│  • Plans execution steps                                    │
│  • Manages human checkpoints                                │
│  • Coordinates specialist agents                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  SPECIALIST AGENTS                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │ Discovery │ │ Analysis │ │ Synthesis│ │ Writing  │      │
│  │  Agent    │ │  Agent   │ │  Agent   │ │  Agent   │      │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘      │
└───────┼─────────────┼───────────┼─────────────┼─────────────┘
        │             │           │             │
┌───────▼─────────────▼───────────▼─────────────▼─────────────┐
│                    TOOL LAYER (MCP)                         │
│  Web Search │ Paper DBs │ PDF Parser │ BibTeX │ LaTeX       │
│  Semantic Scholar │ arXiv │ PubMed │ CrossRef │ Zotero      │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: CLI Core & Research Pipeline (Weeks 1-3)

> **Goal:** Working CLI that can conduct basic research with human checkpoints

### 1.1 Project Restructuring

```
research-tool/
├── src/
│   └── research_tool/           # Main Python package
│       ├── __init__.py
│       ├── cli.py               # Click/Typer CLI entry point
│       ├── core/
│       │   ├── orchestrator.py  # Main agent coordinator
│       │   ├── pipeline.py      # Research pipeline engine
│       │   └── config.py        # Configuration management
│       ├── agents/
│       │   ├── base.py          # Base agent class
│       │   ├── discovery.py     # Literature discovery agent
│       │   ├── analysis.py      # Paper analysis agent
│       │   ├── synthesis.py     # Knowledge synthesis agent
│       │   └── writing.py       # Report generation agent
│       ├── tools/               # MCP-compatible tools
│       │   ├── web_search.py    # Web search (Tavily, Brave)
│       │   ├── paper_search.py  # Academic search (Semantic Scholar, arXiv)
│       │   ├── pdf_parser.py    # PDF extraction
│       │   ├── citation.py      # Citation management
│       │   └── latex.py         # LaTeX compilation
│       ├── memory/              # Knowledge persistence
│       │   ├── project.py       # Research project state
│       │   ├── citations.py     # Citation database
│       │   └── knowledge.py     # RAG/embeddings store
│       └── ui/                  # CLI output formatting
│           ├── progress.py      # Progress bars, spinners
│           ├── interactive.py   # Human checkpoint prompts
│           └── report.py        # Terminal report rendering
├── .agents/skills/              # Existing skills (enhanced)
├── tests/                       # Test suite
├── pyproject.toml               # Modern Python packaging
└── ...
```

### 1.2 CLI Commands

```bash
# Initialize a new research project
research init "AI in Healthcare" --dir ./my-project

# Conduct research (main workflow)
research run "What are the latest advances in federated learning?"
  --depth quick|standard|deep
  --sources arxiv,semantic_scholar,web
  --checkpoint approve|auto
  --output markdown,pdf,docx

# Manage research projects
research project list
research project status <id>
research project export <id> --format pdf

# Literature management
research lit search "transformer architectures"
research lit add paper.pdf
research lit review --topic "attention mechanisms"
research lit matrix --papers paper1,paper2,paper3

# Citation management
research cite add paper.bib
research cite format --style apa
research cite check --document draft.md

# Data extraction
research extract paper.pdf --tables --figures --claims
research extract batch ./papers/ --output ./extractions/

# Report generation
research report generate --template thesis --chapters 6
research report compile --format pdf
research report validate
```

### 1.3 Human-in-the-Loop Checkpoints

```python
# Checkpoint types:
CHECKPOINTS = {
    "plan_approval":    "Review and approve research plan before execution",
    "source_selection": "Choose which sources to prioritize",
    "claim_verification": "Verify extracted claims against sources",
    "draft_review":     "Review generated sections before proceeding",
    "citation_check":   "Verify citations are accurate and complete",
    "final_approval":   "Approve final report before export"
}

# Usage in pipeline:
@checkpoint("plan_approval")
async def approve_plan(plan: ResearchPlan) -> bool:
    """Show plan to user, get approval."""
    display_plan(plan)
    return ask_confirmation("Proceed with this research plan?")
```

### 1.4 Key Deliverables

| File                                     | Purpose                                        |
| ---------------------------------------- | ---------------------------------------------- |
| `src/research_tool/cli.py`               | CLI entry point with all subcommands           |
| `src/research_tool/core/orchestrator.py` | Agent coordination engine                      |
| `src/research_tool/core/pipeline.py`     | Research pipeline with checkpoints             |
| `src/research_tool/agents/*.py`          | 4 specialist agents                            |
| `src/research_tool/tools/*.py`           | 5 core MCP-compatible tools                    |
| `pyproject.toml`                         | Package config with `research` CLI entry point |
| `tests/test_pipeline.py`                 | Pipeline integration tests                     |

---

## Phase 2: Multi-Agent Orchestration & Knowledge Base (Weeks 4-6)

> **Goal:** Parallel agent execution, RAG-based knowledge retrieval, session persistence

### 2.1 Parallel Agent Execution

```python
# Scatter-gather pattern (inspired by GPT-Researcher)
async def deep_research(query: str):
    # 1. Orchestrator generates sub-questions
    sub_questions = await orchestrator.plan(query)

    # 2. Spawn parallel discovery agents
    tasks = [discovery_agent.research(q) for q in sub_questions]
    results = await asyncio.gather(*tasks)

    # 3. Synthesis agent combines findings
    synthesis = await synthesis_agent.combine(results)

    # 4. Human checkpoint
    if not await checkpoint("review_synthesis", synthesis):
        return None

    # 5. Writing agent generates report
    report = await writing_agent.generate(synthesis)
    return report
```

### 2.2 Knowledge Base with RAG

```python
# Vector store for research papers
class KnowledgeBase:
    def __init__(self):
        self.vector_store = ChromaDB()  # Local-first
        self.citations = CitationDB()   # SQLite

    async def index_paper(self, paper: Paper):
        """Index a paper for semantic search."""
        chunks = self.chunk_paper(paper)
        embeddings = await self.embed(chunks)
        self.vector_store.add(embeddings, metadata={
            "title": paper.title,
            "authors": paper.authors,
            "year": paper.year,
            "doi": paper.doi
        })

    async def search(self, query: str, k: int = 10):
        """Semantic search across indexed papers."""
        query_embedding = await self.embed(query)
        return self.vector_store.query(query_embedding, k=k)
```

### 2.3 Session Persistence

```python
# Research session state
@dataclass
class ResearchSession:
    id: str
    query: str
    project_dir: Path
    plan: ResearchPlan
    findings: List[Finding]
    citations: List[Citation]
    draft: Optional[Document]
    checkpoints: List[Checkpoint]
    created_at: datetime
    updated_at: datetime

    def save(self):
        """Persist session to project directory."""
        (self.project_dir / "session.json").write_text(
            self.to_json()
        )

    @classmethod
    def load(cls, project_dir: Path) -> "ResearchSession":
        """Resume a previous session."""
        return cls.from_json(
            (project_dir / "session.json").read_text()
        )
```

### 2.4 Key Deliverables

| File                                       | Purpose                  |
| ------------------------------------------ | ------------------------ |
| `src/research_tool/agents/orchestrator.py` | Multi-agent coordinator  |
| `src/research_tool/memory/knowledge.py`    | RAG-based knowledge base |
| `src/research_tool/memory/session.py`      | Session persistence      |
| `src/research_tool/memory/citations.py`    | Citation database        |
| `tests/test_agents.py`                     | Agent integration tests  |

---

## Phase 3: MCP Server & Extensibility (Weeks 7-9)

> **Goal:** Expose the tool as an MCP server so other AI agents can use it

### 3.1 MCP Server Implementation

```python
# MCP Server exposing research capabilities
from mcp import Server, Tool

server = Server("research-tool")

@server.tool("research_conduct")
async def conduct_research(
    query: str,
    depth: str = "standard",
    sources: List[str] = ["arxiv", "semantic_scholar"],
    human_checkpoint: bool = True
) -> ResearchReport:
    """Conduct deep research on a topic.

    Args:
        query: Research question or topic
        depth: quick, standard, or deep
        sources: Academic databases to search
        human_checkpoint: Require human approval at key steps
    """
    pipeline = ResearchPipeline(query, depth, sources)
    return await pipeline.execute(human_checkpoint)

@server.tool("paper_analyze")
async def analyze_paper(
    paper_path: str,
    extract: List[str] = ["claims", "methods", "findings"]
) -> PaperAnalysis:
    """Analyze a research paper and extract structured information."""
    ...

@server.tool("literature_search")
async def search_literature(
    query: str,
    databases: List[str] = ["semantic_scholar", "arxiv"],
    limit: int = 20
) -> List[Paper]:
    """Search academic literature across multiple databases."""
    ...

@server.tool("citation_manage")
async def manage_citations(
    action: str,
    **kwargs
) -> CitationResult:
    """Add, format, or verify citations."""
    ...
```

### 3.2 Plugin System

```python
# Custom tool registration
class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register(self, name: str, tool: Tool):
        """Register a new research tool."""
        self.tools[name] = tool

    def from_config(self, config_path: Path):
        """Load tools from YAML config."""
        config = yaml.safe_load(config_path.read_text())
        for tool_def in config["tools"]:
            self.register(tool_def["name"], self._load_tool(tool_def))

# Example config (research-tools.yaml):
tools:
  - name: pubmed_search
    module: research_tool.tools.paper_search
    class: PubMedSearch
    config:
      api_key: ${PUBMED_API_KEY}

  - name: zotero_sync
    module: research_tool.tools.citation
    class: ZoteroSync
    config:
      library_id: ${ZOTERO_LIBRARY_ID}
```

### 3.3 Key Deliverables

| File                          | Purpose                    |
| ----------------------------- | -------------------------- |
| `src/research_tool/server.py` | MCP server entry point     |
| `src/research_tool/plugins/`  | Plugin loader and registry |
| `research-tools.yaml`         | Tool configuration         |
| `tests/test_mcp.py`           | MCP server tests           |

---

## Phase 4: Web App Foundation (Weeks 10-12)

> **Goal:** REST API + simple web UI, reusing all Phase 1-3 code

### 4.1 API Layer (FastAPI)

```python
# FastAPI app wrapping the same core logic
from fastapi import FastAPI, BackgroundTasks
from research_tool.core.orchestrator import Orchestrator

app = FastAPI(title="Research Tool API", version="1.0.0")

@app.post("/research/start")
async def start_research(request: ResearchRequest, bg: BackgroundTasks):
    """Start a new research session."""
    session = ResearchSession.create(request.query, request.options)
    bg.add_task(orchestrator.run, session)
    return {"session_id": session.id, "status": "started"}

@app.get("/research/{session_id}/status")
async def get_status(session_id: str):
    """Get research progress."""
    session = ResearchSession.load(session_id)
    return session.status()

@app.get("/research/{session_id}/report")
async def get_report(session_id: str, format: str = "markdown"):
    """Get generated report."""
    session = ResearchSession.load(session_id)
    return session.report(format)

@app.websocket("/research/{session_id}/live")
async def live_updates(websocket, session_id: str):
    """WebSocket for real-time progress updates."""
    ...
```

### 4.2 Simple Web UI

```
┌─────────────────────────────────────────────────────────────┐
│  Research Tool                              [New Project]    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🔍 Research Query                                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ What are the latest advances in federated learning? │   │
│  └─────────────────────────────────────────────────────┘   │
│  [Depth: Standard ▾] [Sources: arXiv, Semantic Scholar ▾]  │
│                                                             │
│  [Start Research]                                           │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  📊 Active Research Session                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ✅ Plan approved (2 min ago)                        │   │
│  │ 🔄 Searching 3 databases...                         │   │
│  │ ⏳ Analysis pending                                  │   │
│  │ ⏳ Synthesis pending                                 │   │
│  │ ⏳ Report generation pending                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [View Report] [Export PDF] [Cite Sources]                  │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Key Deliverables

| File                                 | Purpose                 |
| ------------------------------------ | ----------------------- |
| `src/research_tool/api/`             | FastAPI application     |
| `src/research_tool/api/routes.py`    | API endpoints           |
| `src/research_tool/api/websocket.py` | Real-time updates       |
| `web/`                               | Simple HTML/JS frontend |

---

## Implementation Roadmap

### Timeline Overview

```
Week 1-3:   Phase 1 — CLI Core & Pipeline
            ├── Restructure project as Python package
            ├── Build CLI with Click/Typer
            ├── Implement orchestrator + 4 agents
            ├── Create 5 core MCP tools
            └── Add human checkpoint system

Week 4-6:   Phase 2 — Multi-Agent & Knowledge
            ├── Parallel agent execution
            ├── RAG-based knowledge base
            ├── Session persistence
            └── Citation database

Week 7-9:   Phase 3 — MCP Server
            ├── Expose as MCP server
            ├── Plugin system
            ├── Custom tool registry
            └── Integration tests

Week 10-12: Phase 4 — Web Foundation
            ├── FastAPI REST API
            ├── WebSocket live updates
            ├── Simple web UI
            └── Docker deployment
```

### Priority Matrix

| Feature              | Impact  | Effort  | Priority |
| -------------------- | ------- | ------- | -------- |
| CLI entry point      | 🔴 High | 🟢 Low  | **P0**   |
| Research pipeline    | 🔴 High | 🟡 Med  | **P0**   |
| Human checkpoints    | 🔴 High | 🟡 Med  | **P0**   |
| Paper search tools   | 🔴 High | 🟡 Med  | **P0**   |
| Knowledge base (RAG) | 🟡 Med  | 🔴 High | P1       |
| Session persistence  | 🟡 Med  | 🟢 Low  | P1       |
| MCP server           | 🟡 Med  | 🟡 Med  | P1       |
| Citation management  | 🟡 Med  | 🟡 Med  | P1       |
| Plugin system        | 🟡 Med  | 🔴 High | P2       |
| Web app API          | 🟢 Low  | 🔴 High | P2       |
| Web UI               | 🟢 Low  | 🔴 High | P3       |

---

## Technology Stack

### Phase 1-3 (CLI/Agentic)

| Layer           | Technology           | Rationale                              |
| --------------- | -------------------- | -------------------------------------- |
| Language        | Python 3.11+         | Existing ecosystem, ML libraries       |
| CLI Framework   | Typer + Rich         | Modern, type-safe, beautiful output    |
| Agent Runtime   | Custom (asyncio)     | Full control, no framework lock-in     |
| LLM Integration | LiteLLM              | Multi-provider (OpenAI, Claude, local) |
| Vector DB       | ChromaDB             | Local-first, embedded, simple          |
| Citation DB     | SQLite               | Lightweight, portable                  |
| Web Search      | Tavily API           | AI-optimized search                    |
| Paper Search    | Semantic Scholar API | Free, comprehensive                    |
| PDF Parsing     | PyMuPDF              | Fast, reliable                         |
| LaTeX           | MiKTeX (existing)    | Full TeX support                       |

### Phase 4 (Web App)

| Layer      | Technology              | Rationale                   |
| ---------- | ----------------------- | --------------------------- |
| API        | FastAPI                 | Async, auto-docs, type-safe |
| WebSocket  | FastAPI WS              | Real-time progress          |
| Frontend   | HTMX + Tailwind         | Simple, no build step       |
| Deployment | Docker + docker-compose | Consistent environments     |

---

## Skills Enhancement Plan

### Existing Skills to Enhance

| Skill                   | Enhancement                                 |
| ----------------------- | ------------------------------------------- |
| `deep-research`         | Add MCP tool integration, parallel search   |
| `academic-researcher`   | Add citation database, claim extraction     |
| `pdf`                   | Add batch processing, structured extraction |
| `research-paper-writer` | Add template system, section generation     |
| `latex-paper-en`        | Add auto-compilation, error recovery        |

### New Skills to Create

| Skill                   | Purpose                                   |
| ----------------------- | ----------------------------------------- |
| `research-pipeline`     | Orchestrate full research workflow        |
| `citation-manager`      | BibTeX, citation formatting, verification |
| `paper-analyzer`        | Extract claims, methods, findings         |
| `knowledge-synthesizer` | Combine findings from multiple sources    |
| `human-checkpoint`      | Interactive approval gates                |
| `research-project`      | Project lifecycle management              |

---

## Success Metrics

### Phase 1-3 (CLI/Agentic)

- [ ] `research run "query"` produces a cited research report
- [ ] Human checkpoints pause execution for approval
- [ ] Sessions can be paused and resumed
- [ ] Papers are indexed and searchable via RAG
- [ ] Tool works as MCP server (test with Claude Desktop)

### Phase 4 (Web App)

- [ ] REST API endpoints return same results as CLI
- [ ] WebSocket provides real-time progress updates
- [ ] Web UI shows active research sessions
- [ ] Docker deployment works with one command

---

## Risk Mitigation

| Risk                  | Mitigation                                  |
| --------------------- | ------------------------------------------- |
| LLM API costs         | Cache results, use local models for drafts  |
| Rate limits           | Implement exponential backoff, queue system |
| Large paper corpus    | Chunked indexing, lazy loading              |
| Windows compatibility | Test on Windows CI, use pathlib everywhere  |
| Scope creep           | Strict phase gates, MVP-first approach      |

---

## Next Steps

1. **Immediate (Today)**
    - Create `pyproject.toml` with project metadata
    - Create `src/research_tool/` package structure
    - Implement basic CLI with Typer

2. **This Week**
    - Build orchestrator skeleton
    - Implement paper search tool (Semantic Scholar)
    - Create first human checkpoint

3. **Next Week**
    - Complete 4 specialist agents
    - Add web search tool
    - Test full pipeline end-to-end

---

_This plan is a living document. Update as implementation progresses._
