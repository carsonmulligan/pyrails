"""Controller generator for creating FastAPI routers."""
import sys
from pathlib import Path

from rich.console import Console

from pyrails.utils import camelize, classify, confirm, pluralize, singularize, tableize, underscore

console = Console()


class ControllerGenerator:
    """Generator for creating FastAPI controllers (routers)."""

    ACTIONS = ["index", "show", "create", "update", "destroy"]

    def __init__(self, args: list[str]):
        if not args:
            console.print("[red]Usage:[/red] pyrails generate controller NAME [actions...]")
            sys.exit(1)

        self.controller_name = args[0]
        self.model_name = classify(singularize(self.controller_name))
        self.model_var = underscore(self.model_name)
        self.route_prefix = underscore(self.controller_name)
        self.actions = args[1:] if len(args) > 1 else self.ACTIONS
        self.app_path = Path.cwd()

    def generate(self):
        """Generate controller file."""
        console.print(f"\n[bold green]🔨 Generating controller:[/bold green] {self.controller_name}\n")

        # Check if we're in a PyRails app
        if not (self.app_path / "app" / "controllers").exists():
            console.print("[red]❌ Not in a PyRails application directory[/red]")
            sys.exit(1)

        controller_file = self.app_path / "app" / "controllers" / f"{self.route_prefix}_controller.py"

        # Check if controller exists
        if controller_file.exists():
            if not confirm(f"⚠️  {controller_file.name} already exists. Overwrite?", default=False):
                console.print("[yellow]Aborted.[/yellow]")
                sys.exit(0)

        # Generate controller file
        self._write_controller_file(controller_file)
        console.print(f"   [green]✅[/green] Created {controller_file.relative_to(self.app_path)}")

        # Update application.py to include router
        self._update_application()

        console.print(f"\n[bold green]✨ Controller {self.controller_name} generated successfully![/bold green]")
        console.print(f"\n[bold]Routes available at:[/bold] /api/{self.route_prefix}")

    def _write_controller_file(self, controller_file: Path):
        """Write controller file content."""
        imports = [
            "from fastapi import APIRouter, Depends, HTTPException",
            "from sqlalchemy import select",
            "from sqlalchemy.ext.asyncio import AsyncSession",
            "",
            f"from app.models.{self.model_var} import {self.model_name}",
            "from config.database import get_async_session",
        ]

        router_def = f'''
router = APIRouter(prefix="/api/{self.route_prefix}", tags=["{self.route_prefix}"])
'''

        actions_code = []

        if "index" in self.actions:
            actions_code.append('''

@router.get("/")
async def index(
    session: AsyncSession = Depends(get_async_session)
):
    """List all items."""
    result = await session.execute(select({model_name}))
    items = result.scalars().all()
    return items
'''.format(model_name=self.model_name))

        if "show" in self.actions:
            actions_code.append('''

@router.get("/{item_id}")
async def show(
    item_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Get single item."""
    result = await session.execute(
        select({model_name}).where({model_name}.id == item_id)
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="{model_name} not found")

    return item
'''.format(model_name=self.model_name))

        if "create" in self.actions:
            actions_code.append('''

@router.post("/")
async def create(
    session: AsyncSession = Depends(get_async_session)
):
    """Create new item."""
    # TODO: Add request body parameters
    item = {model_name}()
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item
'''.format(model_name=self.model_name))

        if "update" in self.actions:
            actions_code.append('''

@router.put("/{item_id}")
async def update(
    item_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Update item."""
    result = await session.execute(
        select({model_name}).where({model_name}.id == item_id)
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="{model_name} not found")

    # TODO: Add update logic
    await session.commit()
    await session.refresh(item)
    return item
'''.format(model_name=self.model_name))

        if "destroy" in self.actions:
            actions_code.append('''

@router.delete("/{item_id}")
async def destroy(
    item_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Delete item."""
    result = await session.execute(
        select({model_name}).where({model_name}.id == item_id)
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="{model_name} not found")

    await session.delete(item)
    await session.commit()
    return {{"message": "{model_name} deleted"}}
'''.format(model_name=self.model_name))

        content = f'''"""{self.controller_name} controller - generated by PyRails."""
{chr(10).join(imports)}
{router_def}
{"".join(actions_code)}
'''

        controller_file.write_text(content)

    def _update_application(self):
        """Update config/application.py to include new router."""
        app_file = self.app_path / "config" / "application.py"

        if not app_file.exists():
            console.print(f"   [yellow]⚠️  config/application.py not found[/yellow]")
            return

        content = app_file.read_text()

        import_line = f"from app.controllers.{self.route_prefix}_controller import router as {self.route_prefix}_router"
        include_line = f"app.include_router({self.route_prefix}_router)"

        # Add import
        if import_line not in content:
            # Find a good place to add import (after other controller imports or before app initialization)
            if "from app.controllers" in content:
                # Add after last controller import
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith("from app.controllers"):
                        insert_pos = i + 1
                lines.insert(insert_pos, import_line)
                content = '\n'.join(lines)
            else:
                # Add before app initialization
                content = content.replace(
                    "# Initialize FastAPI app",
                    f"{import_line}\n\n# Initialize FastAPI app"
                )

        # Add router inclusion
        if include_line not in content:
            # Add before final @app.get("/") if it exists, otherwise at the end
            if '@app.get("/")' in content:
                content = content.replace(
                    '@app.get("/")',
                    f'{include_line}\n\n\n@app.get("/")'
                )
            else:
                content += f'\n\n{include_line}\n'

        app_file.write_text(content)
        console.print(f"   [green]✅[/green] Updated config/application.py")
