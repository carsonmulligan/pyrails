# Contributing to PyRails

## Development Setup

```bash
git clone https://github.com/yourusername/pyrails.git
cd pyrails
pip install -e ".[dev]"
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pyrails

# Run specific test
pytest tests/test_cli.py
```

## Testing Your Changes

### Test the CLI

```bash
# Create a test app in a separate directory
cd /tmp
python /path/to/pyrails/bin/pyrails new testapp
cd testapp
python /path/to/pyrails/bin/pyrails generate model Article title:str
python /path/to/pyrails/bin/pyrails db:create
python /path/to/pyrails/bin/pyrails server
```

### Test Generators

```bash
cd testapp
python /path/to/pyrails/bin/pyrails generate model User email:str
python /path/to/pyrails/bin/pyrails generate controller Articles
python /path/to/pyrails/bin/pyrails routes
```

## Code Style

We use Ruff for linting:

```bash
ruff check pyrails/
ruff format pyrails/
```

## Project Structure

```
pyrails/
├── pyrails/
│   ├── cli.py              # Main CLI entry
│   ├── generators/         # Code generators
│   │   ├── app_generator.py
│   │   ├── model_generator.py
│   │   └── controller_generator.py
│   ├── commands/           # CLI commands
│   │   ├── db.py
│   │   ├── server.py
│   │   └── console.py
│   └── utils/              # Utilities
│       ├── inflector.py
│       └── prompts.py
├── tests/                  # Test suite
├── bin/pyrails            # CLI wrapper
└── pyproject.toml
```

## Making Changes

1. **Fork and clone**
   ```bash
   git clone https://github.com/yourusername/pyrails.git
   cd pyrails
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature
   ```

3. **Make changes**
   - Add tests for new features
   - Update documentation
   - Follow existing code style

4. **Test**
   ```bash
   pytest
   ruff check pyrails/
   ```

5. **Commit**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature
   ```

## Adding New Generators

1. Create generator in `pyrails/generators/`
2. Add to CLI in `pyrails/cli.py`
3. Add tests in `tests/generators/`
4. Update documentation

Example generator structure:

```python
class MyGenerator:
    def __init__(self, args: list[str]):
        self.name = args[0]
        self.app_path = Path.cwd()

    def generate(self):
        # Validation
        if not (self.app_path / "app").exists():
            console.print("[red]Not in PyRails app[/red]")
            sys.exit(1)

        # Generate files
        self._write_files()

        # Success message
        console.print("[green]Generated successfully![/green]")
```

## Adding New Commands

1. Create command in `pyrails/commands/`
2. Add to CLI in `pyrails/cli.py`
3. Add tests
4. Update documentation

## Known Issues to Fix

See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for current known issues.

Priority fixes:
1. Controller generator string formatting
2. Import path handling in commands
3. Better error messages

## Questions?

Open an issue or discussion on GitHub.
