"""Admin commands for user management."""
import asyncio
import sys
from pathlib import Path

from rich.console import Console

from pyrails.utils import prompt_text

console = Console()


def create_admin(*args):
    """Create admin user."""
    console.print("\n[bold green]👤 Create Admin User[/bold green]\n")

    # Check if we're in a PyRails app
    if not (Path.cwd() / "config" / "application.py").exists():
        console.print("[red]❌ Not in a PyRails application directory[/red]")
        sys.exit(1)

    email = args[0] if args else prompt_text("Admin email")
    password = prompt_text("Admin password", default="admin123")

    try:
        asyncio.run(_create_admin_async(email, password))
        console.print(f"\n[green]✅ Admin user created:[/green] {email}")
        console.print(f"[dim]Password: {password}[/dim]\n")
    except Exception as e:
        console.print(f"[red]❌ Error creating admin:[/red] {e}")
        sys.exit(1)


async def _create_admin_async(email: str, password: str):
    """Create admin user asynchronously."""
    try:
        from app.models.user import User
    except ImportError:
        console.print("[red]❌ User model not found[/red]")
        console.print("   Generate a User model first:")
        console.print("   pyrails generate model User email:str")
        sys.exit(1)

    from config.database import async_session_maker
    from sqlalchemy import select
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async with async_session_maker() as session:
        # Check if user exists
        result = await session.execute(
            select(User).where(User.email == email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            console.print(f"[yellow]⚠️  User already exists:[/yellow] {email}")
            return

        # Create user
        user = User(
            email=email,
            hashed_password=pwd_context.hash(password),
            is_superuser=True,
            is_active=True,
            is_verified=True,
        )

        session.add(user)
        await session.commit()
