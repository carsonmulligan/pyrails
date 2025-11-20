"""PyRails CLI - Rails-style commands for Python."""
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console

console = Console()


class PyRailsCLI:
    """Main CLI handler for PyRails commands."""

    def __init__(self):
        self.commands = {
            "new": self.new_app,
            "generate": self.generate,
            "g": self.generate,  # Alias
            "server": self.server,
            "s": self.server,  # Alias
            "console": self.console,
            "c": self.console,  # Alias
            "routes": self.routes,
            "db:create": self.db_create,
            "db:migrate": self.db_migrate,
            "db:seed": self.db_seed,
            "db:reset": self.db_reset,
            "admin:create": self.admin_create,
            "setup": self.setup,
            "deploy": self.deploy,
            "help": self.help,
            "--help": self.help,
            "-h": self.help,
        }

    def run(self, args: list[str]):
        """Execute CLI command."""
        if not args:
            self.help()
            sys.exit(1)

        command = args[0]
        command_args = args[1:]

        if command in self.commands:
            try:
                handler = self.commands[command]
                handler(*command_args)
            except Exception as e:
                console.print(f"[red]❌ Error:[/red] {str(e)}")
                sys.exit(1)
        else:
            console.print(f"[red]Unknown command:[/red] {command}")
            self.help()
            sys.exit(1)

    def help(self, *args):
        """Print help message."""
        console.print("""
[bold cyan]PyRails[/bold cyan] - Rails-style CLI for FastAPI

[bold]Usage:[/bold] pyrails COMMAND [options]

[bold yellow]🆕 Generation Commands:[/bold yellow]
  [green]new APP_NAME[/green]           Create a new PyRails application
  [green]generate model NAME[/green]    Generate a new model with migration
  [green]generate controller NAME[/green] Generate a new controller
  [green]generate test NAME[/green]     Generate tests for model/controller
  [green]g[/green]                      Alias for 'generate'

[bold yellow]📦 Database Commands:[/bold yellow]
  [green]db:create[/green]              Create all database tables
  [green]db:migrate[/green]             Run database migrations
  [green]db:seed[/green]                Load seed data
  [green]db:reset[/green]               Drop, create, migrate, and seed (⚠️  destructive!)

[bold yellow]👤 Admin Commands:[/bold yellow]
  [green]admin:create EMAIL[/green]     Create a superuser admin account

[bold yellow]🔧 Setup Commands:[/bold yellow]
  [green]setup stripe[/green]           Configure Stripe API keys
  [green]setup openai[/green]           Configure OpenAI API keys
  [green]setup[/green]                  General configuration wizard

[bold yellow]🚀 Server Commands:[/bold yellow]
  [green]server[/green]                 Start development server on http://localhost:8000
  [green]s[/green]                      Alias for 'server'
  [green]console[/green]                Start interactive Python console with app context
  [green]c[/green]                      Alias for 'console'
  [green]routes[/green]                 Show all registered routes

[bold yellow]☁️  Deployment Commands:[/bold yellow]
  [green]deploy railway[/green]         Deploy to Railway
  [green]deploy fly[/green]             Deploy to Fly.io
  [green]deploy render[/green]          Deploy to Render

[bold]📝 Examples:[/bold]
  pyrails new myapp                          Create new app
  pyrails generate model Article title:str  Generate Article model
  pyrails db:migrate                         Run migrations
  pyrails server                             Start dev server
        """)

    def new_app(self, *args):
        """Generate new PyRails application."""
        from pyrails.generators.app_generator import AppGenerator

        if not args:
            console.print("[red]Usage:[/red] pyrails new APP_NAME")
            sys.exit(1)

        app_name = args[0]
        generator = AppGenerator(app_name)
        generator.generate()

    def generate(self, *args):
        """Generate models, controllers, etc."""
        if not args:
            console.print("[red]Usage:[/red] pyrails generate [model|controller|test] NAME [fields...]")
            sys.exit(1)

        resource_type = args[0]
        resource_args = args[1:]

        if resource_type == "model":
            from pyrails.generators.model_generator import ModelGenerator
            generator = ModelGenerator(resource_args)
            generator.generate()
        elif resource_type == "controller":
            from pyrails.generators.controller_generator import ControllerGenerator
            generator = ControllerGenerator(resource_args)
            generator.generate()
        elif resource_type == "test":
            from pyrails.generators.test_generator import TestGenerator
            generator = TestGenerator(resource_args)
            generator.generate()
        else:
            console.print(f"[red]Unknown generator:[/red] {resource_type}")
            sys.exit(1)

    def server(self, *args):
        """Start development server."""
        from pyrails.commands.server import run_server
        run_server()

    def console(self, *args):
        """Start interactive console."""
        from pyrails.commands.console import run_console
        run_console()

    def routes(self, *args):
        """Show all routes."""
        from pyrails.commands.routes import show_routes
        show_routes()

    def db_create(self, *args):
        """Create database tables."""
        from pyrails.commands.db import create_db
        create_db()

    def db_migrate(self, *args):
        """Run database migrations."""
        from pyrails.commands.db import migrate_db
        migrate_db()

    def db_seed(self, *args):
        """Seed database."""
        from pyrails.commands.db import seed_db
        seed_db()

    def db_reset(self, *args):
        """Reset database (destructive)."""
        from pyrails.commands.db import reset_db
        reset_db()

    def admin_create(self, *args):
        """Create admin user."""
        from pyrails.commands.admin import create_admin
        create_admin(*args)

    def setup(self, *args):
        """Setup configuration."""
        from pyrails.commands.setup import run_setup
        run_setup(*args)

    def deploy(self, *args):
        """Deploy application."""
        from pyrails.commands.deploy import run_deploy
        run_deploy(*args)


def main():
    """Main CLI entry point."""
    cli = PyRailsCLI()
    cli.run(sys.argv[1:])


if __name__ == "__main__":
    main()
