"""Server command for running development server."""
import sys
import subprocess
from pathlib import Path

from rich.console import Console

console = Console()


def run_server(host: str = "0.0.0.0", port: int = 8000):
    """Start development server."""
    console.print("\n[bold green]🚀 Starting PyRails development server...[/bold green]\n")

    # Check if we're in a PyRails app
    if not (Path.cwd() / "config" / "application.py").exists():
        console.print("[red]❌ Not in a PyRails application directory[/red]")
        sys.exit(1)

    # Check for pending migrations (warn but don't block)
    _check_pending_migrations()

    # Check if uvicorn is installed
    try:
        import uvicorn
    except ImportError:
        console.print("[red]❌ uvicorn not found[/red]")
        if _prompt_install("uvicorn[standard]"):
            subprocess.run([sys.executable, "-m", "pip", "install", "uvicorn[standard]"], check=True)
            import uvicorn
        else:
            sys.exit(1)

    console.print(f"[bold cyan]📍 Server running at:[/bold cyan] http://localhost:{port}")
    console.print(f"[bold cyan]📚 API docs:[/bold cyan] http://localhost:{port}/docs")
    console.print(f"[bold cyan]🔧 Admin panel:[/bold cyan] http://localhost:{port}/admin")
    console.print("\n[dim]Press CTRL+C to stop[/dim]\n")

    try:
        uvicorn.run(
            "config.application:app",
            host=host,
            port=port,
            reload=True,
            reload_dirs=["app", "config"],
        )
    except KeyboardInterrupt:
        console.print("\n\n[yellow]👋 Server stopped[/yellow]")


def _check_pending_migrations():
    """Check for pending migrations and warn user."""
    # For now, just check if migrations directory is empty
    migrations_dir = Path.cwd() / "db" / "migrations"

    if migrations_dir.exists():
        migration_files = list(migrations_dir.glob("*.py"))
        if migration_files and not (migrations_dir / "env.py").exists():
            console.print("[yellow]⚠️  Pending migrations detected[/yellow]")
            console.print("   Run: [cyan]pyrails db:migrate[/cyan]\n")


def _prompt_install(package: str) -> bool:
    """Prompt to install missing package."""
    from pyrails.utils import confirm
    return confirm(f"Install {package}?", default=True)
