"""Console command for interactive REPL."""
import sys
from pathlib import Path

from rich.console import Console

console = Console()


def run_console():
    """Start interactive console with app context."""
    console.print("\n[bold green]🐍 Starting PyRails console...[/bold green]\n")

    # Check if we're in a PyRails app
    if not (Path.cwd() / "config" / "application.py").exists():
        console.print("[red]❌ Not in a PyRails application directory[/red]")
        sys.exit(1)

    # Import app context
    try:
        from config.application import app
        from config.database import async_session_maker
        from sqlalchemy import select
        import asyncio

        # Try to import all models
        try:
            from app.models import Base
            import inspect
            import app.models as models_module

            # Collect all model classes
            namespace = {
                "app": app,
                "async_session_maker": async_session_maker,
                "select": select,
                "asyncio": asyncio,
                "Base": Base,
            }

            for name, obj in inspect.getmembers(models_module):
                if inspect.isclass(obj) and hasattr(obj, '__tablename__'):
                    namespace[name] = obj

        except ImportError:
            namespace = {
                "app": app,
                "async_session_maker": async_session_maker,
                "select": select,
                "asyncio": asyncio,
            }

    except Exception as e:
        console.print(f"[red]❌ Error loading app context:[/red] {e}")
        sys.exit(1)

    banner = """
[bold cyan]PyRails Console[/bold cyan]
---------------
Available: app, async_session_maker, select, asyncio, Base

Example - Fetch all records:
  >>> async def get_all(Model):
  ...     async with async_session_maker() as session:
  ...         result = await session.execute(select(Model))
  ...         return result.scalars().all()
  >>> items = asyncio.run(get_all(YourModel))
"""

    console.print(banner)

    # Try IPython first, fall back to standard REPL
    try:
        from IPython import embed
        embed(user_ns=namespace, colors="neutral")
    except ImportError:
        import code
        code.interact(local=namespace, banner="")
