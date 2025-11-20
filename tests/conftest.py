"""Pytest configuration and fixtures."""
import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    tmp = tempfile.mkdtemp()
    yield Path(tmp)
    shutil.rmtree(tmp)


@pytest.fixture
def mock_app_dir(temp_dir):
    """Create a mock PyRails app directory structure."""
    app_dir = temp_dir / "testapp"
    app_dir.mkdir()

    # Create basic structure
    (app_dir / "app" / "models").mkdir(parents=True)
    (app_dir / "app" / "controllers").mkdir(parents=True)
    (app_dir / "config").mkdir()
    (app_dir / "db" / "seeds").mkdir(parents=True)

    # Create __init__ files
    (app_dir / "app" / "__init__.py").touch()
    (app_dir / "app" / "models" / "__init__.py").write_text("from .base import Base\n")
    (app_dir / "app" / "models" / "base.py").write_text(
        "from sqlalchemy.orm import DeclarativeBase\n\n"
        "class Base(DeclarativeBase):\n    pass\n"
    )

    return app_dir
