"""Progress display — spinners, progress bars, and status updates."""

from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Optional

from rich.console import Console
from rich.status import Status
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console()


@contextmanager
def spinner(message: str):
    """Context manager that shows a spinner while working."""
    with console.status(f"[bold cyan]{message}[/]", spinner="dots"):
        yield


def progress_bar(items: list, message: str = "Processing"):
    """Show a progress bar while processing items."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(message, total=len(items))
        for item in items:
            yield item
            progress.advance(task)


def print_section(title: str, content: str) -> None:
    """Print a formatted section."""
    from rich.panel import Panel
    console.print(Panel(content, title=title, border_style="cyan"))


def print_table(headers: list[str], rows: list[list[str]], title: Optional[str] = None) -> None:
    """Print a formatted table."""
    from rich.table import Table

    table = Table(title=title, show_header=True, header_style="bold cyan")
    for header in headers:
        table.add_column(header)
    for row in rows:
        table.add_row(*row)
    console.print(table)


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]✅ {message}[/]")


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]❌ {message}[/]")


def print_warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"[bold yellow]⚠️  {message}[/]")


def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"[bold cyan]ℹ️  {message}[/]")
