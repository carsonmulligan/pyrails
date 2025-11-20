# Installing PyRails

## Quick Install (Recommended)

```bash
pip install git+https://github.com/yourusername/pyrails.git
```

## From Source

```bash
git clone https://github.com/yourusername/pyrails.git
cd pyrails
pip install .
```

## Development Install

```bash
git clone https://github.com/yourusername/pyrails.git
cd pyrails
pip install -e ".[dev]"
```

## Verify Installation

```bash
pyrails --help
```

## Quick Start

```bash
pyrails new myapp
cd myapp
pyrails server
```

Visit http://localhost:8000/docs

## System Requirements

- Python 3.11+
- pip or uv

## What Gets Installed

The `pyrails` command becomes globally available:

```bash
pyrails new          # Create apps
pyrails generate     # Generate code
pyrails db:migrate   # Database commands
pyrails server       # Run server
```

## Troubleshooting

### Command not found

If `pyrails` command isn't found after install:

```bash
# Ensure pip bin directory is in PATH
python -m pyrails.cli --help

# Or create alias
alias pyrails='python -m pyrails.cli'
```

### Import errors

Make sure all dependencies installed:

```bash
pip install -e ".[dev]"
```

### Permission errors

Use --user flag:

```bash
pip install --user git+https://github.com/user/pyrails.git
```

## Uninstall

```bash
pip uninstall pyrails
```
