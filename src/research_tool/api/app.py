"""FastAPI application for the Research Tool.

Provides REST API and WebSocket endpoints for the web UI
and programmatic access to the research platform.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from research_tool import __version__
from research_tool.core.config import load_project_config
from research_tool.core.orchestrator import Orchestrator
from research_tool.memory.session import ResearchSession
from research_tool.tools.paper_search import search_literature


def create_app(project_dir: str = ".") -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Research Tool API",
        description="AI-autonomous research platform with human-in-the-loop control",
        version=__version__,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Store project dir in app state
    app.state.project_dir = Path(project_dir)
    app.state.connections: dict[str, list[WebSocket]] = {}

    # Register routes
    _register_routes(app)
    _register_websocket(app)
    _register_static(app)

    return app


def _register_routes(app: FastAPI) -> None:
    """Register REST API routes."""

    @app.get("/")
    async def index():
        """Serve the web UI."""
        return _get_web_ui()

    @app.get("/api/health")
    async def health():
        """Health check endpoint."""
        return {"status": "ok", "version": __version__}

    @app.get("/api/version")
    async def version():
        """Get version information."""
        return {"version": __version__, "name": "Research Tool"}

    # ── Research endpoints ────────────────────────────────────

    @app.post("/api/research/start")
    async def start_research(request: dict[str, Any]):
        """Start a new research session."""
        query = request.get("query", "")
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")

        depth = request.get("depth", "standard")
        sources = request.get("sources", ["arxiv", "semantic_scholar"])
        auto = request.get("auto", True)

        if isinstance(sources, str):
            sources = [s.strip() for s in sources.split(",")]

        config = load_project_config(app.state.project_dir)
        config.auto_approve = auto

        session = ResearchSession.create(
            query=query,
            project_dir=app.state.project_dir,
            depth=depth,
            sources=sources,
        )

        # Start research in background
        async def _run_research():
            orchestrator = Orchestrator(config, project_dir=app.state.project_dir)
            try:
                result = await asyncio.to_thread(
                    orchestrator.run, query, depth=depth, sources=sources
                )
                await _broadcast(
                    app,
                    session.id,
                    {"type": "completed", "session_id": session.id},
                )
            except Exception as e:
                await _broadcast(
                    app,
                    session.id,
                    {"type": "error", "error": str(e)},
                )

        asyncio.create_task(_run_research())

        return {
            "session_id": session.id,
            "status": "started",
            "query": query,
            "depth": depth,
            "sources": sources,
        }

    @app.get("/api/research/{session_id}/status")
    async def get_status(session_id: str):
        """Get research session status."""
        session_file = app.state.project_dir / "session.json"
        if not session_file.exists():
            raise HTTPException(status_code=404, detail="No active session")

        session = ResearchSession.load(app.state.project_dir)
        return {
            "session_id": session.id,
            "query": session.query,
            "status": session.status,
            "depth": session.depth,
            "sources": session.sources,
            "papers_count": len(session.findings),
            "checkpoints_count": len(session.checkpoints),
            "elapsed": str(session.elapsed_time),
            "created_at": session.created_at,
            "updated_at": session.updated_at,
        }

    @app.get("/api/research/{session_id}/report")
    async def get_report(session_id: str, format: str = "markdown"):
        """Get the generated research report."""
        session_file = app.state.project_dir / "session.json"
        if not session_file.exists():
            raise HTTPException(status_code=404, detail="No active session")

        session = ResearchSession.load(app.state.project_dir)
        if not session.report_path:
            raise HTTPException(status_code=404, detail="Report not yet generated")

        report_path = Path(session.report_path)
        if not report_path.exists():
            raise HTTPException(status_code=404, detail="Report file not found")

        content = report_path.read_text(encoding="utf-8")
        if format == "json":
            return {"content": content, "session_id": session_id}
        return HTMLResponse(content=content, media_type="text/markdown")

    # ── Literature endpoints ──────────────────────────────────

    @app.post("/api/literature/search")
    async def search_papers(request: dict[str, Any]):
        """Search academic literature."""
        query = request.get("query", "")
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")

        databases = request.get("databases", ["arxiv", "semantic_scholar"])
        limit = request.get("limit", 20)
        year_from = request.get("year_from")
        year_to = request.get("year_to")

        if isinstance(databases, str):
            databases = [d.strip() for d in databases.split(",")]

        results = search_literature(
            query,
            databases=databases,
            limit=limit,
            year_from=year_from,
            year_to=year_to,
        )

        return {"query": query, "count": len(results), "results": results}

    # ── Session endpoints ─────────────────────────────────────

    @app.get("/api/sessions")
    async def list_sessions():
        """List all research sessions."""
        sessions = []
        for session_file in app.state.project_dir.rglob("session.json"):
            try:
                session = ResearchSession.load(session_file.parent)
                sessions.append({
                    "session_id": session.id,
                    "query": session.query,
                    "status": session.status,
                    "elapsed": str(session.elapsed_time),
                    "created_at": session.created_at,
                })
            except Exception:
                continue

        return {"count": len(sessions), "sessions": sessions}


async def _broadcast(app: FastAPI, session_id: str, message: dict) -> None:
    """Broadcast a message to all WebSocket connections for a session."""
    connections = app.state.connections.get(session_id, [])
    dead = []
    for ws in connections:
        try:
            await ws.send_json(message)
        except Exception:
            dead.append(ws)
    for ws in dead:
        connections.remove(ws)


def _register_websocket(app: FastAPI) -> None:
    """Register WebSocket endpoint for live updates."""

    @app.websocket("/ws/research/{session_id}")
    async def websocket_research(websocket: WebSocket, session_id: str):
        """WebSocket endpoint for real-time research progress."""
        await websocket.accept()

        # Register connection
        if session_id not in app.state.connections:
            app.state.connections[session_id] = []
        app.state.connections[session_id].append(websocket)

        try:
            while True:
                # Keep connection alive and handle client messages
                data = await websocket.receive_text()
                msg = json.loads(data)

                if msg.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
                elif msg.get("type") == "get_status":
                    session_file = app.state.project_dir / "session.json"
                    if session_file.exists():
                        session = ResearchSession.load(app.state.project_dir)
                        await websocket.send_json({
                            "type": "status",
                            "status": session.status,
                            "papers_count": len(session.findings),
                        })
        except WebSocketDisconnect:
            app.state.connections[session_id].remove(websocket)


def _register_static(app: FastAPI) -> None:
    """Register static file serving for web UI assets."""
    static_dir = Path(__file__).parent.parent.parent.parent / "web" / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


def _get_web_ui() -> str:
    """Return the main web UI HTML."""
    web_dir = Path(__file__).parent.parent.parent.parent / "web"
    index_file = web_dir / "index.html"
    if index_file.exists():
        return index_file.read_text(encoding="utf-8")
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Research Tool v{__version__}</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-900 text-white min-h-screen">
    <div class="max-w-4xl mx-auto py-12 px-6">
        <h1 class="text-4xl font-bold mb-2">🧠 Research Tool</h1>
        <p class="text-gray-400 mb-8">v{__version__} — API is running</p>
        <div class="bg-gray-800 rounded-lg p-6">
            <h2 class="text-xl font-semibold mb-4">API Endpoints</h2>
            <ul class="space-y-2 text-sm font-mono">
                <li><span class="text-green-400">GET</span>  /api/health</li>
                <li><span class="text-green-400">GET</span>  /api/version</li>
                <li><span class="text-blue-400">POST</span> /api/research/start</li>
                <li><span class="text-green-400">GET</span>  /api/research/{{id}}/status</li>
                <li><span class="text-green-400">GET</span>  /api/research/{{id}}/report</li>
                <li><span class="text-blue-400">POST</span> /api/literature/search</li>
                <li><span class="text-green-400">GET</span>  /api/sessions</li>
                <li><span class="text-purple-400">WS</span>   /ws/research/{{id}}</li>
            </ul>
        </div>
        <p class="text-gray-500 mt-4 text-sm">
            Full web UI available in <code>web/index.html</code>
        </p>
    </div>
</body>
</html>"""
