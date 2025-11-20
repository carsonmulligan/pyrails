"""App generator for creating new PyRails applications."""
import os
import subprocess
import sys
from pathlib import Path

from rich.console import Console

from pyrails.utils import select_option, confirm

console = Console()


class AppGenerator:
    """Generator for creating new PyRails applications."""

    TEMPLATES = [
        ("empty", "Bare structure with no models"),
        ("blog", "User + Article models with CRUD"),
        ("chat", "OpenAI-compatible chat with vanilla JS frontend"),
        ("saas", "Multi-tenant with User + Organization + Stripe"),
        ("saas-chat", "Combined SaaS + Chat features"),
        ("api", "API-only, no templates/views"),
    ]

    DATABASES = [
        ("sqlite", "SQLite (recommended for development)"),
        ("postgresql", "PostgreSQL (recommended for production)"),
    ]

    def __init__(self, app_name: str):
        self.app_name = app_name
        self.app_path = Path.cwd() / app_name
        self.template = None
        self.database = None

    def generate(self):
        """Generate the application."""
        console.print(f"\n[bold green]🚀 Creating PyRails app:[/bold green] {self.app_name}\n")

        # Check if directory exists
        if self.app_path.exists():
            console.print(f"[red]❌ Directory already exists:[/red] {self.app_path}")
            sys.exit(1)

        # Interactive prompts
        self._prompt_template()
        self._prompt_database()

        # Create directory structure
        self._create_structure()

        # Generate files based on template
        self._generate_files()

        # Initialize git
        if confirm("\n📦 Initialize git repository?", default=True):
            self._init_git()

        # Setup dependencies
        self._setup_dependencies()

        # Final message
        self._print_success()

    def _prompt_template(self):
        """Prompt for template selection."""
        self.template = select_option(
            "Choose a template:",
            self.TEMPLATES,
            default=0
        )
        console.print(f"[green]✅ Selected template:[/green] {self.template}")

    def _prompt_database(self):
        """Prompt for database selection."""
        self.database = select_option(
            "Choose a database:",
            self.DATABASES,
            default=0
        )
        console.print(f"[green]✅ Selected database:[/green] {self.database}")

    def _create_structure(self):
        """Create directory structure."""
        console.print(f"\n[cyan]📁 Creating directory structure...[/cyan]")

        directories = [
            "app/models",
            "app/controllers",
            "app/services",
            "app/views",
            "app/assets/css",
            "app/assets/js",
            "config",
            "db/seeds",
            "db/migrations",
            "tests",
            "data",
        ]

        for directory in directories:
            (self.app_path / directory).mkdir(parents=True, exist_ok=True)
            console.print(f"   [green]✅[/green] Created {directory}/")

    def _generate_files(self):
        """Generate application files."""
        console.print(f"\n[cyan]📝 Generating application files...[/cyan]")

        # Generate core config files
        self._write_pyproject_toml()
        self._write_env_file()
        self._write_env_example()
        self._write_gitignore()
        self._write_readme()

        # Generate config files
        self._write_settings()
        self._write_database()
        self._write_application()

        # Generate base model
        self._write_base_model()

        # Generate __init__ files
        self._write_init_files()

        # Generate template-specific files
        if self.template == "empty":
            pass  # Just structure
        elif self.template == "blog":
            self._generate_blog_template()
        elif self.template == "chat":
            self._generate_chat_template()
        elif self.template == "saas":
            self._generate_saas_template()
        elif self.template == "saas-chat":
            self._generate_saas_template()
            self._generate_chat_template()
        elif self.template == "api":
            self._generate_api_template()

        console.print(f"   [green]✅[/green] Generated all application files")

    def _write_pyproject_toml(self):
        """Write pyproject.toml."""
        db_deps = ""
        if self.database == "postgresql":
            db_deps = '\n    "asyncpg>=0.29.0",'

        content = f'''[project]
name = "{self.app_name}"
version = "0.1.0"
description = "PyRails application"
requires-python = ">=3.11"

dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "sqlalchemy>=2.0.0",
    "alembic>=1.13.0",
    "aiosqlite>=0.20.0",{db_deps}
    "fastapi-users[sqlalchemy]>=13.0.0",
    "sqladmin>=0.19.0",
    "jinja2>=3.1.4",
    "python-dotenv>=1.0.0",
    "pydantic-settings>=2.5.0",
    "passlib[bcrypt]>=1.7.4",
    "python-multipart>=0.0.20",
    "python-jose[cryptography]>=3.3.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py311"
'''
        self._write_file("pyproject.toml", content)

    def _write_env_file(self):
        """Write .env file."""
        db_url = "sqlite+aiosqlite:///./data/app.db"
        if self.database == "postgresql":
            db_url = "postgresql+asyncpg://user:password@localhost/dbname"

        content = f'''# Application
APP_NAME="{self.app_name}"
DEBUG=true
SECRET_KEY="change-this-to-a-random-secret-key-in-production"

# Database
DATABASE_URL="{db_url}"

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
'''
        self._write_file(".env", content)

    def _write_env_example(self):
        """Write .env.example file."""
        content = '''# Application
APP_NAME="your-app-name"
DEBUG=true
SECRET_KEY="your-secret-key-here"

# Database
DATABASE_URL="sqlite+aiosqlite:///./data/app.db"
# DATABASE_URL="postgresql+asyncpg://user:password@localhost/dbname"

# CORS
CORS_ORIGINS=["http://localhost:3000"]
'''
        self._write_file(".env.example", content)

    def _write_gitignore(self):
        """Write .gitignore."""
        content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# PyRails
data/
*.db

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Environment
.env

# Distribution
dist/
build/
*.egg-info/
'''
        self._write_file(".gitignore", content)

    def _write_readme(self):
        """Write README.md."""
        content = f'''# {self.app_name}

A PyRails application.

## Getting Started

```bash
# Install dependencies
uv sync
# or
pip install -e .

# Run migrations
pyrails db:migrate

# Seed database
pyrails db:seed

# Start server
pyrails server
```

## Available Commands

- `pyrails server` - Start development server
- `pyrails db:migrate` - Run database migrations
- `pyrails db:seed` - Load seed data
- `pyrails console` - Interactive console
- `pyrails routes` - Show all routes

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

## Admin Panel

Visit http://localhost:8000/admin for the admin panel.
'''
        self._write_file("README.md", content)

    def _write_settings(self):
        """Write config/settings.py."""
        content = '''"""Application settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    # Application
    APP_NAME: str = "PyRails App"
    DEBUG: bool = False
    SECRET_KEY: str

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/app.db"

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]


settings = Settings()
'''
        self._write_file("config/settings.py", content)

    def _write_database(self):
        """Write config/database.py."""
        content = '''"""Database configuration."""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config.settings import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

# Create session maker
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for async database sessions."""
    async with async_session_maker() as session:
        yield session
'''
        self._write_file("config/database.py", content)

    def _write_application(self):
        """Write config/application.py."""
        content = '''"""Main FastAPI application."""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.models.base import Base
from config.database import engine
from config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown events."""
    # Startup: Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database initialized")

    yield

    # Shutdown: Close database connections
    await engine.dispose()
    print("👋 Application shutdown")


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
    debug=settings.DEBUG,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
static_dir = Path(__file__).parent.parent / "app" / "assets"
if static_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(static_dir)), name="assets")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "docs": "/docs",
        "version": "1.0.0"
    }
'''
        self._write_file("config/application.py", content)

    def _write_base_model(self):
        """Write app/models/base.py."""
        content = '''"""Base model for all SQLAlchemy models."""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all models."""
    pass
'''
        self._write_file("app/models/base.py", content)

    def _write_init_files(self):
        """Write __init__.py files."""
        self._write_file("config/__init__.py", "")
        self._write_file("app/__init__.py", "")
        self._write_file("app/models/__init__.py", "from .base import Base\n")
        self._write_file("app/controllers/__init__.py", "")
        self._write_file("app/services/__init__.py", "")
        self._write_file("db/__init__.py", "")
        self._write_file("db/seeds/__init__.py", "")
        self._write_file("tests/__init__.py", "")

    def _generate_blog_template(self):
        """Generate blog template files."""
        # Will be implemented with model/controller generators
        pass

    def _generate_chat_template(self):
        """Generate chat template files."""
        # Will be implemented with chat-specific generators
        pass

    def _generate_saas_template(self):
        """Generate SaaS template files."""
        # Will be implemented with SaaS-specific generators
        pass

    def _generate_api_template(self):
        """Generate API template files."""
        # Will be implemented with API-specific generators
        pass

    def _init_git(self):
        """Initialize git repository."""
        console.print(f"\n[cyan]📦 Initializing git repository...[/cyan]")
        try:
            subprocess.run(["git", "init"], cwd=self.app_path, check=True, capture_output=True)
            subprocess.run(["git", "add", "."], cwd=self.app_path, check=True, capture_output=True)
            subprocess.run(
                ["git", "commit", "-m", "Initial PyRails app"],
                cwd=self.app_path,
                check=True,
                capture_output=True
            )
            console.print(f"   [green]✅[/green] Git repository initialized")
        except subprocess.CalledProcessError as e:
            console.print(f"   [yellow]⚠️  Git initialization failed: {e}[/yellow]")

    def _setup_dependencies(self):
        """Setup dependencies with uv or pip."""
        console.print(f"\n[cyan]📦 Setting up dependencies...[/cyan]")

        # Check if uv is available
        try:
            subprocess.run(["uv", "--version"], capture_output=True, check=True)
            console.print("   [green]✅[/green] Found uv package manager")

            if confirm("Install dependencies with uv?", default=True):
                try:
                    subprocess.run(["uv", "sync"], cwd=self.app_path, check=True)
                    console.print("   [green]✅[/green] Dependencies installed")
                except subprocess.CalledProcessError:
                    console.print("   [yellow]⚠️  Failed to install dependencies[/yellow]")
        except (subprocess.CalledProcessError, FileNotFoundError):
            console.print("   [yellow]💡 uv not found. Install dependencies manually:[/yellow]")
            console.print(f"      cd {self.app_name} && pip install -e .")

    def _print_success(self):
        """Print success message."""
        console.print(f"\n[bold green]✨ Successfully created {self.app_name}![/bold green]\n")
        console.print("[bold]Next steps:[/bold]")
        console.print(f"  cd {self.app_name}")
        console.print(f"  pyrails db:migrate")
        console.print(f"  pyrails server")
        console.print(f"\n[bold cyan]🚀 Your app will be available at:[/bold cyan] http://localhost:8000")
        console.print(f"[bold cyan]📚 API docs:[/bold cyan] http://localhost:8000/docs\n")

    def _write_file(self, path: str, content: str):
        """Write content to file."""
        file_path = self.app_path / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
