#!/usr/bin/env python3
"""
Environment Check Script for Research Tool.

Verifies all required tools, packages, and dependencies needed for
AI-assisted research tasks including:
  - Code writing & running (Python, Node.js)
  - LaTeX compilation (MiKTeX)
  - Web search & browser automation
  - Data extraction (PDF, DOCX, CSV, XLSX, images → text/markdown)
  - MCP server availability

Usage:
    python scripts/check_environment.py          # standard output
    python scripts/check_environment.py --json   # JSON output for CI
    python scripts/check_environment.py --verbose  # detailed diagnostics

Exit codes:
    0 — All checks passed (or only warnings)
    1 — Critical checks failed
"""

import argparse
import contextlib
import importlib.util
import json
import os
import platform
import re
import shutil
import subprocess
import sys

# ── Force UTF-8 output (Windows console defaults to cp1252, which cannot
# ── encode the box-drawing/emoji characters used below) ─────────────────────
if sys.platform == "win32":
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleOutputCP(65001)
        kernel32.SetConsoleCP(65001)
    except Exception:  # noqa: BLE001 - best-effort
        pass
for _stream in (sys.stdout, sys.stderr):
    _reconfigure = getattr(_stream, "reconfigure", None)
    if _reconfigure is not None:
        with contextlib.suppress(Exception):
            _reconfigure(encoding="utf-8", errors="replace")

# ── ANSI Colors ──────────────────────────────────────────────────────────────

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

PASS_ICON = "✅"
WARN_ICON = "⚠️ "
FAIL_ICON = "❌"
INFO_ICON = "ℹ️ "

# ── Configuration ────────────────────────────────────────────────────────────

REQUIRED_PYTHON_PACKAGES = {
    "pandas": "data manipulation / CSV/XLSX analysis",
    "numpy": "numerical computing",
    "scipy": "scientific computing / hypothesis testing",
    "matplotlib": "plotting / chart generation",
    "seaborn": "statistical visualization",
    "pymupdf": "PDF text extraction (import fitz)",
    "docx": "DOCX read/write (import docx)",
    "openpyxl": "XLSX read/write",
    "PIL": "image processing (import PIL; install pillow)",
    "requests": "HTTP client / web scraping",
    "bs4": "HTML parsing (import bs4; install beautifulsoup4)",
    "lxml": "XML/HTML parser",
}

OPTIONAL_PYTHON_PACKAGES = {
    "pytesseract": "OCR from images",
    "transformers": "NLP / ML models",
    "scikit-learn": "machine learning toolkit",
    "tabulate": "markdown table formatting",
    "markdownify": "HTML to Markdown conversion",
}

REQUIRED_NPM_PACKAGES = {
    "docx": "Word document generation",
    "pptxgenjs": "PowerPoint generation",
    "markdown-it": "Markdown rendering",
    "@playwright/test": "Browser automation",
}

OPTIONAL_NPM_PACKAGES = {
    "playwright-core": "Playwright core",
}

REQUIRED_CLI_TOOLS = {
    "python": "Python interpreter",
    "pip": "Python package manager",
    "node": "Node.js runtime",
    "npm": "Node.js package manager",
}

OPTIONAL_CLI_TOOLS = {
    "latex": "LaTeX compiler",
    "pdflatex": "PDFLaTeX compiler",
    "latexmk": "LaTeX build automation",
    "git": "Version control",
    "npx": "Node package runner",
}

# ── Helpers ──────────────────────────────────────────────────────────────────


def cprint(text: str, color: str = "", bold: bool = False, end: str = "\n"):
    """Print with ANSI color, falling back to plain text if not a TTY."""
    if not sys.stdout.isatty():
        # Strip ANSI codes for non-TTY output
        clean = re.sub(r"\033\[[0-9;]*m", "", text)
        print(clean, end=end)
        return
    prefix = color
    if bold:
        prefix += BOLD
    print(f"{prefix}{text}{RESET}", end=end)


def run_cmd(cmd: list, timeout: int = 15) -> tuple:
    """Run a command and return (returncode, stdout, stderr)."""
    # Resolve the executable via PATH. On Windows, bare names like `npm`
    # can resolve to an extensionless shim that CreateProcess cannot run,
    # while `shutil.which` correctly finds `npm.cmd`.
    resolved = list(cmd)
    if resolved:
        exe = shutil.which(resolved[0])
        if exe:
            resolved[0] = exe
    try:
        proc = subprocess.run(
            resolved, capture_output=True, text=True, timeout=timeout
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except FileNotFoundError:
        return -1, "", "Command not found"
    except subprocess.TimeoutExpired:
        return -1, "", "Timed out"
    except Exception as e:
        return -1, "", str(e)


def check_version(cmd: list, flag: str = "--version") -> str:
    """Extract version string from a command's --version output."""
    rc, out, err = run_cmd(cmd + [flag])
    if rc != 0:
        return ""
    # Take the first line that looks like a version string
    for line in (out or err or "").split("\n"):
        line = line.strip()
        # Skip common noise
        if (
            not line
            or "WARNING" in line.upper()
            or "copyright" in line.lower()
            or "This is free software" in line
        ):
            continue
        if re.match(r".*\d+\.\d+", line):
            return line[:80]
    return line[:60] if line else out[:60] if out else err[:60]


def check_python_package(pkg_name: str, import_name: str = None) -> tuple:
    """Check if a Python package is installed. Returns (found, version)."""
    import_name = import_name or pkg_name.lower()
    rc, out, err = run_cmd(
        [sys.executable, "-c", f"import {import_name}; print({import_name}.__version__)"]
    )
    if rc == 0 and out:
        return True, out.strip()[:30]
    # Fallback: try pip show
    rc2, out2, err2 = run_cmd(
        [sys.executable, "-m", "pip", "show", pkg_name]
    )
    if rc2 == 0 and out2:
        for line in out2.split("\n"):
            if line.startswith("Version:"):
                return True, line.split(":", 1)[1].strip()[:30]
    return False, ""


def check_npm_package(pkg_name: str) -> tuple:
    """Check if an npm package is installed. Returns (found, version)."""
    rc, out, err = run_cmd(
        ["npm", "list", "--json", "--depth=0", pkg_name]
    )
    if rc == 0 and out:
        try:
            data = json.loads(out)
            if "dependencies" in data and pkg_name in data["dependencies"]:
                ver = data["dependencies"][pkg_name].get("version", "")
                return True, ver
        except json.JSONDecodeError:
            pass
    return False, ""


def find_latex() -> list:
    """Find LaTeX compilers by checking common install locations."""
    found = []
    candidates = [
        "latex.exe",
        "pdflatex.exe",
        "xelatex.exe",
        "lualatex.exe",
        "latexmk.exe",
    ]
    for exe in candidates:
        path = shutil.which(exe)
        if path:
            rc, out, _ = run_cmd([exe, "--version"])
            ver_line = ""
            if rc == 0 and out:
                ver_line = out.split("\n")[0][:60] if out else ""
            found.append({"exe": exe, "path": path, "version": ver_line})

    # Also check common MiKTeX install paths
    common_paths = [
        os.path.join(os.environ.get("PROGRAMFILES", "C:\\Program Files"), "MiKTeX", "miktex", "bin", "x64"),
        os.path.join(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)"), "MiKTeX", "miktex", "bin", "x64"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "MiKTeX", "miktex", "bin", "x64"),
    ]
    for path in common_paths:
        if os.path.isdir(path):
            for exe in candidates:
                full_path = os.path.join(path, exe)
                if os.path.isfile(full_path) and not shutil.which(exe):
                    found.append({"exe": exe, "path": full_path, "version": "found (not in PATH)"})

    return found


def check_mcp_servers() -> list:
    """Check MCP server configurations."""
    results = []
    mcp_json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".vscode", "mcp.json")

    servers_expected = {
        "filesystem": "File system access",
        "sequential-thinking": "Structured reasoning",
        "puppeteer": "Browser automation",
        "brave-search": "Web search",
        "multi-mcp": "Multi-model code review",
        "blind-auditor": "Code auditing",
    }

    mcp_servers_configured = {}
    if os.path.isfile(mcp_json_path):
        try:
            with open(mcp_json_path) as f:
                mcp_data = json.load(f)
            mcp_servers_configured = mcp_data.get("servers", {})
        except (OSError, json.JSONDecodeError):
            pass

    for name, description in servers_expected.items():
        if name in mcp_servers_configured:
            server_config = mcp_servers_configured[name]
            cmd = server_config.get("command", "")
            # Check if the command is available
            cmd_path = shutil.which(cmd) if cmd else None
            if cmd_path or cmd == "npx":
                results.append(
                    {"name": name, "description": description, "status": "configured", "command": cmd}
                )
            else:
                results.append(
                    {"name": name, "description": description, "status": "command-not-found", "command": cmd}
                )
        else:
            results.append(
                {"name": name, "description": description, "status": "not-configured", "command": ""}
            )

    return results


# ── Report ────────────────────────────────────────────────────────────────────


class CheckReport:
    def __init__(self):
        self.entries = []
        self.critical_failures = 0
        self.warnings = 0

    def add(self, category: str, name: str, status: str, detail: str, critical: bool = False):
        self.entries.append({
            "category": category,
            "name": name,
            "status": status,       # "pass", "warn", "fail", "info"
            "detail": detail,
            "critical": critical,
        })
        if status == "fail" and critical:
            self.critical_failures += 1
        elif status == "warn":
            self.warnings += 1

    def print_summary(self, verbose: bool = False):
        cprint("\n╔═══════════════════════════════════════════════════════════╗", CYAN, bold=True)
        cprint("║      Research Tool — Environment Check Report             ║", CYAN, bold=True)
        cprint("╚═══════════════════════════════════════════════════════════╝", CYAN, bold=True)
        cprint(f"  System: {platform.system()} {platform.release()} ({platform.machine()})", INFO_ICON)
        cprint("")

        current_category = ""
        for entry in self.entries:
            if entry["category"] != current_category:
                current_category = entry["category"]
                cprint(f"\n── {current_category} ──", BOLD)

            icon = PASS_ICON if entry["status"] == "pass" else (
                WARN_ICON if entry["status"] == "warn" else (
                    FAIL_ICON if entry["status"] == "fail" else INFO_ICON
                )
            )
            color = GREEN if entry["status"] == "pass" else (
                YELLOW if entry["status"] == "warn" else (
                    RED if entry["status"] == "fail" else CYAN
                )
            )
            line = f"  {icon} {entry['name']}: {entry['detail']}"
            if entry["status"] == "fail" and entry["critical"]:
                line += " [REQUIRED]"
            cprint(line, color)

        cprint("")
        cprint("─" * 55, CYAN)
        cprint(f"  Critical failures: {self.critical_failures}", RED if self.critical_failures > 0 else GREEN)
        cprint(f"  Warnings:          {self.warnings}", YELLOW if self.warnings > 0 else GREEN)
        cprint(f"  Status:            {'ALL CHECKS PASSED' if self.critical_failures == 0 else 'SOME CHECKS FAILED'}", GREEN if self.critical_failures == 0 else RED)
        cprint("─" * 55, CYAN)

        if self.critical_failures > 0:
            cprint("\n  ❌ Some critical requirements are missing.", RED, bold=True)
            cprint("     See SETUP.md for installation instructions.\n", YELLOW)

    def to_json(self) -> str:
        return json.dumps(
            {
                "system": platform.system(),
                "python_version": platform.python_version(),
                "entries": self.entries,
                "critical_failures": self.critical_failures,
                "warnings": self.warnings,
                "passed": self.critical_failures == 0,
            },
            indent=2,
        )


# ── Main Checks ──────────────────────────────────────────────────────────────


def run_checks(verbose: bool = False) -> CheckReport:
    report = CheckReport()

    # ── 1. System & Runtimes ──────────────────────────────────────────────
    # Python
    py_ver = platform.python_version()
    py_major, py_minor = map(int, py_ver.split(".")[:2])
    if py_major >= 3 and py_minor >= 10:
        report.add("System & Runtimes", "Python", "pass", f"{py_ver} (≥3.10 ✓)", critical=True)
    else:
        report.add("System & Runtimes", "Python", "fail", f"{py_ver} (need ≥3.10)", critical=True)

    # Pip / uv (package manager)
    rc, out, _ = run_cmd([sys.executable, "-m", "pip", "--version"])
    if rc == 0 and out:
        ver = out.split()[1] if len(out.split()) > 1 else "found"
        report.add("System & Runtimes", "pip", "pass", ver, critical=True)
    else:
        # uv-based venvs (created with `uv venv`) have no pip — that's fine
        rc_uv, out_uv, _ = run_cmd(["uv", "--version"])
        if rc_uv == 0 and out_uv:
            report.add("System & Runtimes", "pip", "pass", f"uv ({out_uv.strip()})", critical=True)
        else:
            report.add("System & Runtimes", "pip", "fail", "not found (install pip or uv)", critical=True)

    # Node.js
    node_ver = check_version(["node"])
    if node_ver:
        # Check version >= 18
        match = re.search(r"v?(\d+)", node_ver)
        if match and int(match.group(1)) >= 18:
            report.add("System & Runtimes", "Node.js", "pass", node_ver, critical=True)
        else:
            report.add("System & Runtimes", "Node.js", "warn", f"{node_ver} (need ≥18)", critical=True)
    else:
        report.add("System & Runtimes", "Node.js", "fail", "not found", critical=True)

    # npm
    npm_ver = check_version(["npm"])
    if npm_ver:
        report.add("System & Runtimes", "npm", "pass", npm_ver, critical=True)
    else:
        report.add("System & Runtimes", "npm", "fail", "not found", critical=True)

    # Git
    git_ver = check_version(["git"])
    if git_ver:
        report.add("System & Runtimes", "Git", "pass", git_ver)
    else:
        report.add("System & Runtimes", "Git", "warn", "not found (optional for version control)")

    # ── 2. Python Packages ────────────────────────────────────────────────
    for pkg, purpose in REQUIRED_PYTHON_PACKAGES.items():
        import_name = {"bs4": "bs4", "PIL": "PIL"}.get(pkg, pkg)
        found, ver = check_python_package(pkg, import_name)
        if found:
            report.add("Python Packages (Required)", purpose, "pass", f"{pkg} {ver}")
        else:
            report.add("Python Packages (Required)", purpose, "warn", f"{pkg} not installed — needed for {purpose}")

    for pkg, purpose in OPTIONAL_PYTHON_PACKAGES.items():
        found, ver = check_python_package(pkg, pkg)
        if found:
            report.add("Python Packages (Optional)", purpose, "pass", f"{pkg} {ver}")
        else:
            report.add("Python Packages (Optional)", purpose, "info", f"{pkg} not installed — optional for {purpose}")

    # ── 3. npm Packages ──────────────────────────────────────────────────
    for pkg, purpose in REQUIRED_NPM_PACKAGES.items():
        found, ver = check_npm_package(pkg)
        if found:
            report.add("npm Packages (Required)", purpose, "pass", f"{pkg} {ver}")
        else:
            report.add("npm Packages (Required)", purpose, "warn", f"{pkg} not installed — needed for {purpose}")

    for pkg, purpose in OPTIONAL_NPM_PACKAGES.items():
        found, ver = check_npm_package(pkg)
        if found:
            report.add("npm Packages (Optional)", purpose, "pass", f"{pkg} {ver}")

    # ── 4. LaTeX / MiKTeX ─────────────────────────────────────────────────
    latex_found = find_latex()
    if latex_found:
        for item in latex_found:
            ver_str = item["version"] if item["version"] else "found"
            report.add("LaTeX / MiKTeX", f"{item['exe']}", "pass", f"{ver_str}")
    else:
        report.add("LaTeX / MiKTeX", "LaTeX compiler", "warn", "No LaTeX installation found — needed for .tex compilation")

    # Check specific LaTeX tools
    for tool in ["latexmk", "bibtex"]:
        path = shutil.which(tool)
        if path:
            report.add("LaTeX / MiKTeX", tool, "pass", f"found at {path}")
        else:
            report.add("LaTeX / MiKTeX", tool, "warn", f"{tool} not found — needed for bibliography/build automation")

    # ── 5. Data Extraction Tools ──────────────────────────────────────────
    # Test PDF extraction
    try:
        import fitz
        report.add("Data Extraction", "PDF → Text (PyMuPDF)", "pass", fitz.__version__)
    except ImportError:
        report.add("Data Extraction", "PDF → Text (PyMuPDF)", "warn", "pymupdf not installed")

    # Test DOCX extraction
    try:
        import docx
        report.add("Data Extraction", "DOCX → Text (python-docx)", "pass", docx.__version__)
    except ImportError:
        report.add("Data Extraction", "DOCX → Text (python-docx)", "warn", "python-docx not installed")

    # Test XLSX extraction
    try:
        import openpyxl
        report.add("Data Extraction", "XLSX → CSV/MD (openpyxl)", "pass", openpyxl.__version__)
    except ImportError:
        report.add("Data Extraction", "XLSX → CSV/MD (openpyxl)", "warn", "openpyxl not installed")

    # Test OCR
    try:
        import PIL
        report.add("Data Extraction", "Image → Text (Pillow)", "pass", PIL.__version__)
    except ImportError:
        report.add("Data Extraction", "Image → Text (Pillow)", "warn", "pillow not installed")

    # Tesseract OCR
    tess_path = shutil.which("tesseract")
    if tess_path:
        rc, out, _ = run_cmd(["tesseract", "--version"])
        ver_str = out.split("\n")[0][:60] if out else "found"
        report.add("Data Extraction", "OCR (Tesseract)", "pass", ver_str)
    else:
        report.add("Data Extraction", "OCR (Tesseract)", "info", "tesseract not found — optional for OCR")

    # CSV → Markdown
    try:
        import tabulate
        report.add("Data Extraction", "CSV/XLSX → Markdown (tabulate)", "pass", tabulate.__version__)
    except ImportError:
        report.add("Data Extraction", "CSV/XLSX → Markdown (tabulate)", "info", "tabulate not installed — optional for markdown conversion")

    # HTML → Markdown
    if importlib.util.find_spec("markdownify"):
        report.add("Data Extraction", "HTML/Web → Markdown (markdownify)", "pass", "found")
    else:
        report.add("Data Extraction", "HTML/Web → Markdown (markdownify)", "info", "markdownify not installed — optional for web→md")

    # ── 6. Web Search & Browser ───────────────────────────────────────────
    # Playwright
    playwright_path = shutil.which("playwright") or shutil.which("npx")
    if playwright_path:
        rc, out, _ = run_cmd(["npx", "playwright", "--version"])
        if rc == 0 and out:
            report.add("Web & Browser", "Playwright", "pass", f"v{out}")
        else:
            # Check if it's installed in node_modules
            playwright_installed, _ = check_npm_package("@playwright/test")
            if playwright_installed:
                report.add("Web & Browser", "Playwright", "pass", "found in node_modules")
            else:
                report.add("Web & Browser", "Playwright", "warn", "@playwright/test not installed — needed for browser automation")

    # Puppeteer MCP
    puppeteer_mcp = shutil.which("mcp-server-puppeteer")
    if puppeteer_mcp:
        report.add("Web & Browser", "Puppeteer MCP", "pass", "found")
    else:
        report.add("Web & Browser", "Puppeteer MCP", "info", "mcp-server-puppeteer not found — optional for browser MCP")

    # Requests (web scraping)
    try:
        import requests
        ver = requests.__version__
        report.add("Web & Browser", "Web Scraping (requests+bs4)", "pass", f"requests {ver}")
        try:
            import bs4
            report.add("Web & Browser", "HTML Parsing (beautifulsoup4)", "pass", bs4.__version__)
        except ImportError:
            report.add("Web & Browser", "HTML Parsing (beautifulsoup4)", "warn", "beautifulsoup4 not installed")
    except ImportError:
        report.add("Web & Browser", "Web Scraping", "warn", "requests not installed")

    # ── 7. MCP Servers ────────────────────────────────────────────────────
    mcp_results = check_mcp_servers()
    for mcp in mcp_results:
        if mcp["status"] == "configured":
            report.add("MCP Servers", mcp["name"], "pass", f"configured ({mcp['description']})")
        elif mcp["status"] == "command-not-found":
            report.add("MCP Servers", mcp["name"], "warn", f"configured but command '{mcp['command']}' not found")
        else:
            report.add("MCP Servers", mcp["name"], "info", f"not configured ({mcp['description']})")

    # ── 8. Virtual Environment ────────────────────────────────────────────
    in_venv = sys.prefix != sys.base_prefix
    if in_venv:
        report.add("Environment", "Virtual Env Active", "pass", sys.prefix)
    else:
        report.add("Environment", "Virtual Env Active", "warn", "No virtual environment active — run: .venv\\Scripts\\Activate.ps1")

    return report


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Check environment for research tool dependencies"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Show detailed diagnostics"
    )
    args = parser.parse_args()

    report = run_checks(verbose=args.verbose)

    if args.json:
        print(report.to_json())
    else:
        report.print_summary(verbose=args.verbose)

    return 1 if report.critical_failures > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
