# PyRails

Convention over configuration web framework for FastAPI. Rails-inspired CLI and structure for Python's async ecosystem.

## Installation

```bash
pip install pyrails
```

Or install from source:

```bash
git clone https://github.com/yourusername/pyrails.git
cd pyrails
pip install -e .
```

## Quick Start

```bash
pyrails new myapp
cd myapp
pyrails generate model Article title:str body:text
pyrails db:migrate
pyrails server
```

Visit `http://localhost:8000/docs` for API documentation.

## Commands

### Generation
```bash
pyrails new APP_NAME              # Create new app
pyrails generate model NAME ...   # Generate model + migration
pyrails generate controller NAME  # Generate controller
pyrails g                         # Alias for generate
```

### Database
```bash
pyrails db:create     # Create tables
pyrails db:migrate    # Run migrations
pyrails db:seed       # Load seed data
pyrails db:reset      # Reset database
```

### Development
```bash
pyrails server        # Start dev server (alias: s)
pyrails console       # Interactive REPL (alias: c)
pyrails routes        # Show all routes
```

### Setup
```bash
pyrails setup stripe  # Configure Stripe keys
pyrails setup openai  # Configure OpenAI keys
```

## Templates

- `empty` - Bare structure
- `blog` - User + Article models
- `chat` - OpenAI chat with vanilla JS
- `saas` - Multi-tenant with Stripe
- `api` - API-only

## Field Types

`str`, `text`, `int`, `float`, `bool`, `datetime`, `date`, `json`, `references`

Example:
```bash
pyrails generate model Post title:str body:text author:references
```

## Project Structure

```
myapp/
├── app/
│   ├── models/       # SQLAlchemy models
│   ├── controllers/  # FastAPI routers
│   ├── services/     # Business logic
│   └── views/        # Templates
├── config/
│   ├── application.py
│   ├── database.py
│   └── settings.py
├── db/
│   ├── seeds/
│   └── migrations/
└── tests/
```

## Contributing

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Development Setup

```bash
git clone https://github.com/yourusername/pyrails.git
cd pyrails
pip install -e ".[dev]"
pytest
```

## Documentation

- [Framework Architecture](CLAUDE.md)
- [API Reference](docs/api.md)
- [Tutorial](docs/tutorial.md)

## License

MIT
