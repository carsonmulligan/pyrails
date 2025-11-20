.PHONY: install test lint format clean demo help

help:
	@echo "PyRails Development Commands"
	@echo ""
	@echo "  make install    Install package in dev mode"
	@echo "  make test       Run test suite"
	@echo "  make lint       Run linter"
	@echo "  make format     Format code"
	@echo "  make clean      Clean build artifacts"
	@echo "  make demo       Create demo app"

install:
	pip install -e ".[dev]"

test:
	pytest -v

lint:
	ruff check pyrails/

format:
	ruff format pyrails/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache .ruff_cache

demo:
	@echo "Creating demo app in /tmp/pyrails-demo"
	@cd /tmp && python -m pyrails.cli new pyrails-demo <<< "1\n1\ny\nn" && cd pyrails-demo && pwd
