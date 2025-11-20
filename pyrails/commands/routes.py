"""Routes command for displaying all registered routes."""
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()


def show_routes():
    """Show all registered routes."""
    console.print("\n[bold green]📋 PyRails Routes[/bold green]\n")

    # Check if we're in a PyRails app
    if not (Path.cwd() / "config" / "application.py").exists():
        console.print("[red]❌ Not in a PyRails application directory[/red]")
        sys.exit(1)

    try:
        from config.application import app

        table = Table(title="Application Routes")
        table.add_column("Method", style="cyan")
        table.add_column("Path", style="magenta")
        table.add_column("Name", style="green")
        table.add_column("Handler", style="yellow")

        for route in app.routes:
            if hasattr(route, "methods") and hasattr(route, "path"):
                for method in route.methods:
                    table.add_row(
                        method,
                        route.path,
                        route.name or "",
                        route.endpoint.__name__ if hasattr(route, "endpoint") else ""
                    )

        console.print(table)
        console.print()

    except Exception as e:
        console.print(f"[red]❌ Error loading routes:[/red] {e}")
        sys.exit(1)
