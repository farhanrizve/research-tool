<#
.SYNOPSIS
    Research Tool Environment Setup Script
.DESCRIPTION
    Sets up Python virtual environment, installs dependencies, and configures
    MCP servers for AI-assisted research workflows.
.NOTES
    Run from the repository root: .\scripts\setup_env.ps1
#>

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSCommandPath)
Set-Location $RepoRoot

Write-Host "╔════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   Research Tool - Environment Setup        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ── Step 1: Check prerequisites ──────────────────────────────────────────────
Write-Host "[1/5] Checking prerequisites..." -ForegroundColor Yellow

# Check Python
try {
    $pyVersion = python --version 2>&1
    Write-Host "  ✅ Python: $pyVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Python not found. Install Python 3.10+ from https://python.org" -ForegroundColor Red
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "  ✅ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Node.js not found. Install Node.js 18+ from https://nodejs.org" -ForegroundColor Red
    exit 1
}

# Check uv (package manager — preferred) or pip
try {
    $uvVersion = uv --version 2>&1
    Write-Host "  ✅ uv: $uvVersion" -ForegroundColor Green
    $UseUv = $true
} catch {
    try {
        $pipVersion = pip --version 2>&1
        Write-Host "  ✅ pip: $($pipVersion.Split()[1])" -ForegroundColor Green
        $UseUv = $false
    } catch {
        Write-Host "  ❌ Neither uv nor pip found. Install uv (https://docs.astral.sh/uv/) or pip." -ForegroundColor Red
        exit 1
    }
}

# Check git
try {
    $gitVersion = git --version 2>&1
    Write-Host "  ✅ Git: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Git not found. Some features will be unavailable." -ForegroundColor Yellow
}

Write-Host ""

# ── Step 2: Python virtual environment ───────────────────────────────────────
Write-Host "[2/5] Setting up Python virtual environment..." -ForegroundColor Yellow

if (Test-Path ".venv") {
    Write-Host "  ℹ Virtual environment already exists." -ForegroundColor Yellow
} else {
    if ($UseUv) {
        uv venv .venv
    } else {
        python -m venv .venv
    }
    Write-Host "  ✅ Created .venv" -ForegroundColor Green
}

# Install the package (editable) with all extras
if ($UseUv) {
    uv pip install -e ".[all]" -q
    Write-Host "  ✅ research-tool installed (uv)" -ForegroundColor Green
} else {
    $pip = Join-Path $RepoRoot ".venv\Scripts\pip.exe"
    & $pip install --upgrade pip -q
    Write-Host "  ✅ pip upgraded" -ForegroundColor Green
    & $pip install -e ".[all]" -q
    Write-Host "  ✅ research-tool installed (pip)" -ForegroundColor Green
}

Write-Host ""

# ── Step 3: Install Python packages ──────────────────────────────────────────
Write-Host "[3/5] Installing Python packages..." -ForegroundColor Yellow

$pythonPackages = @(
    "pandas",
    "numpy",
    "scipy",
    "matplotlib",
    "seaborn",
    "scikit-learn",
    "jupyter",
    "nbformat",
    "openpyxl",
    "python-docx",
    "graphviz",
    "pillow",
    "requests",
    "beautifulsoup4",
    "lxml",
    "pymupdf",
    "transformers",
    "datasets",
    "tqdm"
)

foreach ($pkg in $pythonPackages) {
    Write-Host "  Installing $pkg..." -NoNewline
    try {
        if ($UseUv) {
            uv pip install $pkg -q
        } else {
            & $pip install $pkg -q --no-warn-script-location
        }
        Write-Host " ✅" -ForegroundColor Green
    } catch {
        Write-Host " ❌ Failed" -ForegroundColor Red
    }
}

Write-Host ""

# ── Step 4: Install Node.js packages ─────────────────────────────────────────
Write-Host "[4/5] Installing Node.js packages..." -ForegroundColor Yellow

if (Test-Path "package.json") {
    npm install --silent 2>$null
    Write-Host "  ✅ npm packages installed" -ForegroundColor Green
} else {
    Write-Host "  ℹ No package.json found. Skipping." -ForegroundColor Yellow
}

Write-Host ""

# ── Step 5: Install MCP servers (optional) ───────────────────────────────────
Write-Host "[5/5] Setting up MCP servers (optional)..." -ForegroundColor Yellow

$mcpDir = Join-Path $RepoRoot ".mcp-servers"
if (-not (Test-Path $mcpDir)) {
    New-Item -ItemType Directory -Path $mcpDir -Force | Out-Null
}

# Multi-MCP
$multiDir = Join-Path $mcpDir "multi_mcp"
if (-not (Test-Path $multiDir)) {
    Write-Host "  ℹ Multi-MCP: Not cloned. To install:" -ForegroundColor Yellow
    Write-Host "     git clone https://github.com/religa/multi_mcp.git `"$multiDir`"" -ForegroundColor Gray
    Write-Host "     cd `"$multiDir`" && uv sync && cp .env.example .env" -ForegroundColor Gray
} else {
    Write-Host "  ✅ Multi-MCP: Found" -ForegroundColor Green
}

# Blind-Auditor
$blindDir = Join-Path $mcpDir "Blind-Auditor"
if (-not (Test-Path $blindDir)) {
    Write-Host "  ℹ Blind-Auditor: Not cloned. To install:" -ForegroundColor Yellow
    Write-Host "     git clone https://github.com/Sim-xia/Blind-Auditor.git `"$blindDir`"" -ForegroundColor Gray
    Write-Host "     cd `"$blindDir`" && uv sync" -ForegroundColor Gray
} else {
    Write-Host "  ✅ Blind-Auditor: Found" -ForegroundColor Green
}

# Create .env from .env.example if exists
$multiEnv = Join-Path $multiDir ".env"
$multiEnvExample = Join-Path $multiDir ".env.example"
if ((Test-Path $multiEnvExample) -and -not (Test-Path $multiEnv)) {
    Copy-Item $multiEnvExample $multiEnv
    Write-Host "  ✅ Created .env for Multi-MCP (edit to add API keys)" -ForegroundColor Green
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   Setup Complete!                           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Activate environment: .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  2. Edit .\.venv\mcp-servers\multi_mcp\.env to add API keys" -ForegroundColor White
Write-Host "  3. See AGENTS.md for how to use AI research skills" -ForegroundColor White
Write-Host ""
