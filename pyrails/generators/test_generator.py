"""Test generator for creating test files."""
import sys
from pathlib import Path

from rich.console import Console

from pyrails.utils import classify, confirm, singularize, tableize, underscore

console = Console()


class TestGenerator:
    """Generator for creating test files."""

    def __init__(self, args: list[str]):
        if not args:
            console.print("[red]Usage:[/red] pyrails generate test MODEL_NAME")
            sys.exit(1)

        self.name = args[0]
        self.model_name = classify(singularize(self.name))
        self.model_var = underscore(self.model_name)
        self.table_name = tableize(self.name)
        self.app_path = Path.cwd()

    def generate(self):
        """Generate test file."""
        console.print(f"\n[bold green]🔨 Generating tests:[/bold green] {self.model_name}\n")

        test_file = self.app_path / "tests" / f"test_{self.model_var}.py"

        if test_file.exists():
            if not confirm(f"⚠️  {test_file.name} already exists. Overwrite?", default=False):
                console.print("[yellow]Aborted.[/yellow]")
                sys.exit(0)

        self._write_test_file(test_file)
        console.print(f"   [green]✅[/green] Created {test_file.relative_to(self.app_path)}")

        console.print(f"\n[bold green]✨ Tests generated successfully![/bold green]")
        console.print(f"\n[bold]Run tests with:[/bold] pytest tests/test_{self.model_var}.py")

    def _write_test_file(self, test_file: Path):
        """Write test file content."""
        content = f'''"""Tests for {self.model_name} model."""
import pytest
from app.models.{self.model_var} import {self.model_name}


@pytest.mark.asyncio
async def test_create_{self.model_var}(db_session):
    """Test creating a {self.model_name}."""
    item = {self.model_name}()
    db_session.add(item)
    await db_session.commit()
    await db_session.refresh(item)

    assert item.id is not None
    assert item.created_at is not None


@pytest.mark.asyncio
async def test_{self.model_var}_repr(db_session):
    """Test {self.model_name} __repr__."""
    item = {self.model_name}()
    db_session.add(item)
    await db_session.commit()
    await db_session.refresh(item)

    assert f"<{self.model_name} {{item.id}}>" == repr(item)
'''

        test_file.write_text(content)
