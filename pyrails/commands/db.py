"""Database commands for PyRails."""
import asyncio
import sys
from pathlib import Path

from rich.console import Console

from pyrails.utils import confirm

console = Console()


def create_db():
    """Create database tables."""
    console.print("\n[cyan]🔨 Creating database tables...[/cyan]")

    try:
        asyncio.run(_create_db_async())
        console.print("[green]✅ Database tables created[/green]\n")
    except Exception as e:
        console.print(f"[red]❌ Error creating database:[/red] {e}")
        sys.exit(1)


async def _create_db_async():
    """Create database tables asynchronously."""
    # Import here to avoid issues when not in project
    from app.models.base import Base
    from config.database import engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def migrate_db():
    """Run database migrations."""
    console.print("\n[cyan]🔄 Running database migrations...[/cyan]")

    alembic_ini = Path.cwd() / "alembic.ini"

    if not alembic_ini.exists():
        console.print("[yellow]⚠️  alembic.ini not found[/yellow]")
        console.print("   Creating Alembic configuration...")
        _init_alembic()

    try:
        import alembic.config
        alembic_args = [
            '--raiseerr',
            '-c', str(alembic_ini),
            'upgrade', 'head',
        ]
        alembic.config.main(argv=alembic_args)
        console.print("[green]✅ Migrations completed[/green]\n")
    except Exception as e:
        console.print(f"[red]❌ Error running migrations:[/red] {e}")
        # For now, just use db:create
        console.print("[yellow]💡 Using db:create instead...[/yellow]")
        create_db()


def seed_db():
    """Seed database."""
    console.print("\n[cyan]🌱 Seeding database...[/cyan]")

    seed_file = Path.cwd() / "db" / "seeds" / "development.py"

    if not seed_file.exists():
        console.print(f"[yellow]⚠️  Seed file not found:[/yellow] {seed_file}")
        console.print("   Create db/seeds/development.py with an async seed() function")
        return

    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("seeds", seed_file)
        seeds = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(seeds)

        if hasattr(seeds, 'seed'):
            asyncio.run(seeds.seed())
            console.print("[green]✅ Database seeded successfully[/green]\n")
        else:
            console.print(f"[red]❌ No seed() function found in {seed_file}[/red]")
    except Exception as e:
        console.print(f"[red]❌ Error seeding database:[/red] {e}")
        sys.exit(1)


def reset_db():
    """Reset database (drop, create, migrate, seed)."""
    console.print("\n[bold yellow]⚠️  WARNING: This will destroy all data![/bold yellow]")

    if not confirm("Continue with database reset?", default=False):
        console.print("[yellow]Aborted.[/yellow]")
        return

    console.print("\n[cyan]🔄 Resetting database...[/cyan]")

    try:
        asyncio.run(_reset_db_async())
        console.print("[green]✅ Database reset complete[/green]\n")
    except Exception as e:
        console.print(f"[red]❌ Error resetting database:[/red] {e}")
        sys.exit(1)


async def _reset_db_async():
    """Reset database asynchronously."""
    from app.models.base import Base
    from config.database import engine

    # Drop all tables
    console.print("   Dropping all tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # Create tables
    console.print("   Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed
    seed_file = Path.cwd() / "db" / "seeds" / "development.py"
    if seed_file.exists():
        console.print("   Seeding database...")
        import importlib.util
        spec = importlib.util.spec_from_file_location("seeds", seed_file)
        seeds = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(seeds)

        if hasattr(seeds, 'seed'):
            await seeds.seed()


def _init_alembic():
    """Initialize Alembic configuration."""
    # This would create alembic.ini and env.py
    # For now, this is handled by model generator
    pass
