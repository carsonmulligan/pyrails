"""Model generator for creating SQLAlchemy models."""
import re
import sys
from datetime import datetime
from pathlib import Path

from rich.console import Console

from pyrails.utils import camelize, classify, confirm, tableize, underscore

console = Console()


class ModelGenerator:
    """Generator for creating SQLAlchemy models with migrations."""

    FIELD_TYPE_MAP = {
        "str": "String(255)",
        "string": "String(255)",
        "text": "Text",
        "int": "Integer",
        "integer": "Integer",
        "float": "Float",
        "bool": "Boolean",
        "boolean": "Boolean",
        "datetime": "DateTime",
        "date": "Date",
        "json": "JSON",
    }

    def __init__(self, args: list[str]):
        if not args:
            console.print("[red]Usage:[/red] pyrails generate model NAME [field:type...]")
            sys.exit(1)

        self.model_name = classify(args[0])
        self.table_name = tableize(args[0])
        self.app_path = Path.cwd()
        self.references = []
        self.fields = self._parse_fields(args[1:])

    def generate(self):
        """Generate model and migration files."""
        console.print(f"\n[bold green]🔨 Generating model:[/bold green] {self.model_name}\n")

        # Check if we're in a PyRails app
        if not (self.app_path / "app" / "models").exists():
            console.print("[red]❌ Not in a PyRails application directory[/red]")
            console.print("   Run this command from your PyRails app root")
            sys.exit(1)

        model_file = self.app_path / "app" / "models" / f"{underscore(self.model_name)}.py"

        # Check if model exists
        if model_file.exists():
            if not confirm(f"⚠️  {model_file.name} already exists. Overwrite?", default=False):
                console.print("[yellow]Aborted.[/yellow]")
                sys.exit(0)

        # Generate model file
        self._write_model_file(model_file)
        console.print(f"   [green]✅[/green] Created {model_file.relative_to(self.app_path)}")

        # Update __init__.py
        self._update_models_init()

        # Update related models for references
        if self.references:
            self._update_related_models()

        # Generate migration
        self._generate_migration()

        console.print(f"\n[bold green]✨ Model {self.model_name} generated successfully![/bold green]")
        console.print(f"\n[bold]Next steps:[/bold]")
        console.print(f"  pyrails db:migrate")

    def _parse_fields(self, field_args: list[str]) -> list[dict]:
        """Parse field definitions from arguments."""
        fields = []

        for field_arg in field_args:
            if ":" not in field_arg:
                console.print(f"[yellow]⚠️  Skipping invalid field:[/yellow] {field_arg}")
                continue

            name, field_type = field_arg.split(":", 1)

            if field_type == "references" or field_type.endswith(":references"):
                # Handle references (foreign keys)
                ref_model = classify(name)
                ref_table = tableize(name)
                fields.append({
                    "name": f"{underscore(name)}_id",
                    "type": "Integer",
                    "reference": {
                        "model": ref_model,
                        "table": ref_table,
                        "field": name,
                    }
                })
                self.references.append({
                    "model": ref_model,
                    "field": name,
                    "back_populates": tableize(self.model_name),
                })
            elif field_type in self.FIELD_TYPE_MAP:
                fields.append({
                    "name": name,
                    "type": self.FIELD_TYPE_MAP[field_type],
                })
            else:
                console.print(f"[yellow]⚠️  Unknown field type:[/yellow] {field_type}, using String(255)")
                fields.append({
                    "name": name,
                    "type": "String(255)",
                })

        return fields

    def _write_model_file(self, model_file: Path):
        """Write model file content."""
        imports = ["from datetime import datetime", "from sqlalchemy import Column, Integer, DateTime"]

        # Add field type imports
        field_types = set()
        for field in self.fields:
            if field["type"] == "String(255)":
                field_types.add("String")
            elif field["type"] in ["Text", "Float", "Boolean", "Date", "JSON"]:
                field_types.add(field["type"])
            if "reference" in field:
                field_types.add("ForeignKey")

        if field_types:
            imports.append(f"from sqlalchemy import {', '.join(sorted(field_types))}")

        if self.references:
            imports.append("from sqlalchemy.orm import relationship")

        imports.append("from .base import Base")

        # Build field definitions
        field_defs = ['    id = Column(Integer, primary_key=True)']

        for field in self.fields:
            if "reference" in field:
                ref = field["reference"]
                field_defs.append(
                    f'    {field["name"]} = Column(Integer, ForeignKey("{ref["table"]}.id"), '
                    f'nullable=False, index=True)'
                )
            else:
                field_defs.append(f'    {field["name"]} = Column({field["type"]}, nullable=False)')

        # Add timestamps
        field_defs.extend([
            "",
            "    # Timestamps",
            "    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)",
            "    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)",
        ])

        # Add relationships
        if self.references:
            field_defs.append("")
            field_defs.append("    # Relationships")
            for ref in self.references:
                field_defs.append(
                    f'    {ref["field"]} = relationship("{ref["model"]}", '
                    f'back_populates="{ref["back_populates"]}")'
                )

        content = f'''"""{self.model_name} model - generated by PyRails."""
{chr(10).join(imports)}


class {self.model_name}(Base):
    """{self.model_name} model."""
    __tablename__ = "{self.table_name}"

{chr(10).join(field_defs)}

    def __repr__(self):
        return f"<{self.model_name} {{self.id}}>"
'''

        model_file.write_text(content)

    def _update_models_init(self):
        """Update app/models/__init__.py to include new model."""
        init_file = self.app_path / "app" / "models" / "__init__.py"
        content = init_file.read_text()

        import_line = f"from .{underscore(self.model_name)} import {self.model_name}"

        if import_line not in content:
            # Add import after Base import
            if "from .base import Base" in content:
                content = content.replace(
                    "from .base import Base\n",
                    f"from .base import Base\n{import_line}\n"
                )
            else:
                content += f"\n{import_line}\n"

            init_file.write_text(content)
            console.print(f"   [green]✅[/green] Updated app/models/__init__.py")

    def _update_related_models(self):
        """Update related models to add back-references."""
        for ref in self.references:
            model_file = self.app_path / "app" / "models" / f"{underscore(ref['model'])}.py"

            if not model_file.exists():
                console.print(f"   [yellow]⚠️  Related model not found:[/yellow] {model_file.name}")
                continue

            content = model_file.read_text()

            # Check if relationship already exists
            rel_line = f'{ref["back_populates"]} = relationship("{self.model_name}"'
            if rel_line in content:
                continue

            # Add relationship import if needed
            if "from sqlalchemy.orm import relationship" not in content:
                content = content.replace(
                    "from sqlalchemy import",
                    "from sqlalchemy.orm import relationship\nfrom sqlalchemy import"
                )

            # Find where to add the relationship (before __repr__)
            if "def __repr__" in content:
                # Add before __repr__
                relationship_code = f'\n    # Relationships\n    {ref["back_populates"]} = relationship("{self.model_name}", back_populates="{ref["field"]}")\n'
                content = content.replace(
                    "    def __repr__",
                    f"{relationship_code}\n    def __repr__"
                )
            else:
                # Add at end of class
                relationship_code = f'\n    # Relationships\n    {ref["back_populates"]} = relationship("{self.model_name}", back_populates="{ref["field"]}")\n'
                # Find last line with indentation in class
                lines = content.split('\n')
                for i in range(len(lines) - 1, -1, -1):
                    if lines[i].startswith('    ') and lines[i].strip():
                        lines.insert(i + 1, relationship_code)
                        break
                content = '\n'.join(lines)

            model_file.write_text(content)
            console.print(f"   [green]✅[/green] Updated {model_file.name} with relationship")

    def _generate_migration(self):
        """Generate Alembic migration file."""
        migrations_dir = self.app_path / "db" / "migrations"
        migrations_dir.mkdir(parents=True, exist_ok=True)

        # Create alembic.ini if it doesn't exist
        alembic_ini = self.app_path / "alembic.ini"
        if not alembic_ini.exists():
            self._create_alembic_config()

        # For now, just create a placeholder migration
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        migration_file = migrations_dir / f"{timestamp}_create_{self.table_name}.py"

        migration_content = f'''"""Create {self.table_name} table.

Revision ID: {timestamp}
Create Date: {datetime.now().isoformat()}
"""
from alembic import op
import sqlalchemy as sa


def upgrade():
    """Create {self.table_name} table."""
    # Migration will be auto-generated when you run: pyrails db:migrate
    pass


def downgrade():
    """Drop {self.table_name} table."""
    op.drop_table("{self.table_name}")
'''

        migration_file.write_text(migration_content)
        console.print(f"   [green]✅[/green] Created migration: {migration_file.name}")

    def _create_alembic_config(self):
        """Create Alembic configuration files."""
        alembic_ini_content = '''[alembic]
script_location = db/migrations
prepend_sys_path = .
version_path_separator = os

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
'''
        alembic_ini = self.app_path / "alembic.ini"
        alembic_ini.write_text(alembic_ini_content)

        # Create env.py for migrations
        env_py_content = '''"""Alembic environment configuration."""
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Import Base and all models
from app.models import Base
from config.settings import settings

config = context.config

# Set SQLAlchemy URL from settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode using async."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
'''
        env_file = self.app_path / "db" / "migrations" / "env.py"
        env_file.write_text(env_py_content)

        console.print(f"   [green]✅[/green] Created Alembic configuration")
