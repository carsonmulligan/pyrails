# PyRails

Convention over configuration web framework for FastAPI. Rails-inspired CLI and structure for Python's async ecosystem.

## Installation

```bash
# From GitHub
pip install git+https://github.com/yourusername/pyrails.git

# From source
git clone https://github.com/yourusername/pyrails.git
cd pyrails
pip install .
```

See [INSTALL.md](INSTALL.md) for more options.

## Quick Start

```bash
pyrails new blog
cd blog
pyrails generate model Post title:str body:text
pyrails db:migrate
pyrails server
```

Visit `http://localhost:8000/docs`

## Commands

```bash
pyrails new APP              # Create app
pyrails g model NAME ...     # Generate model + migration
pyrails g controller NAME    # Generate controller  
pyrails db:migrate           # Run migrations
pyrails server               # Start dev server
pyrails console              # Interactive REPL
```

See [QUICKSTART.md](QUICKSTART.md) for full command reference.

## Features

- Rails-style CLI with colon notation (`db:migrate`)
- Interactive app creation with templates
- Auto-generating migrations with models
- Async-first (FastAPI + SQLAlchemy 2.0)
- Convention over configuration
- Multiple templates (blog, chat, SaaS, API)

## Templates

- **empty** - Bare structure
- **blog** - User + Article
- **chat** - OpenAI with vanilla JS
- **saas** - Multi-tenant + Stripe
- **api** - API-only

## Field Types

`str`, `text`, `int`, `float`, `bool`, `datetime`, `date`, `json`, `references`

Example:
```bash
pyrails g model Post title:str author:references published:bool
```

## Documentation

- [INSTALL.md](INSTALL.md) - Installation guide
- [QUICKSTART.md](QUICKSTART.md) - Quick reference
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development setup
- [CLAUDE.md](CLAUDE.md) - Architecture details
- [PUBLISHING.md](PUBLISHING.md) - PyPI publication

## Development

```bash
git clone https://github.com/yourusername/pyrails.git
cd pyrails
make install    # Install with dev dependencies
make test       # Run tests
make lint       # Lint code
make demo       # Create demo app
```

## Testing

```bash
# Run test suite
pytest

# Test installation
./test_install.sh

# Test pip install
./test_pip_install.sh
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT
