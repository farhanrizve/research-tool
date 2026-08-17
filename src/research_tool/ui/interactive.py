"""Human checkpoint system — interactive approval gates.

This is the core human-in-the-loop mechanism. Checkpoints pause execution
and present information to the user for review before proceeding.
"""

from __future__ import annotations

import sys
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

console = Console()


def checkpoint(
    checkpoint_type: str,
    title: str,
    content: str,
    auto_approve: bool = False,
) -> bool:
    """Present a checkpoint to the user and get approval.

    Args:
        checkpoint_type: Type of checkpoint (plan_approval, review_synthesis, etc.)
        title: Display title for the checkpoint
        content: Content to display for review
        auto_approve: If True, skip the prompt and auto-approve

    Returns:
        True if approved, False if rejected
    """
    if auto_approve:
        return True

    console.print()
    console.print(Panel(
        content,
        title=f"⏸️  {title}",
        subtitle=f"Checkpoint: {checkpoint_type}",
        border_style="yellow",
        padding=(1, 2),
    ))

    try:
        approved = Confirm.ask(
            "[bold yellow]Proceed?[/]",
            default=True,
        )
    except (KeyboardInterrupt, EOFError):
        console.print("\n[dim]Checkpoint cancelled by user.[/]")
        return False

    if not approved:
        console.print("[red]❌ Checkpoint rejected. Stopping pipeline.[/]")

    return approved


def checkpoint_with_options(
    checkpoint_type: str,
    title: str,
    content: str,
    options: list[str],
    auto_approve: bool = False,
) -> Optional[str]:
    """Present a checkpoint with multiple choice options.

    Args:
        checkpoint_type: Type of checkpoint
        title: Display title
        content: Content to display
        options: List of option labels
        auto_approve: If True, return the first option

    Returns:
        Selected option label, or None if cancelled
    """
    if auto_approve:
        return options[0] if options else None

    console.print()
    console.print(Panel(
        content,
        title=f"⏸️  {title}",
        subtitle=f"Checkpoint: {checkpoint_type}",
        border_style="yellow",
        padding=(1, 2),
    ))

    for i, opt in enumerate(options, 1):
        console.print(f"  [bold cyan]{i}.[/] {opt}")

    try:
        choice = input(f"\n  Select option (1-{len(options)}) [1]: ").strip()
        idx = int(choice) - 1 if choice else 0
        if 0 <= idx < len(options):
            return options[idx]
        console.print("[red]Invalid choice.[/]")
        return None
    except (KeyboardInterrupt, EOFError, ValueError):
        console.print("\n[dim]Checkpoint cancelled.[/]")
        return None
