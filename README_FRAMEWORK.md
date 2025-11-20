# PyRails

A Rails-inspired web framework built on FastAPI that brings Ruby on Rails' developer experience to Python.

## Features

- 🚀 **Rails-like CLI** with commands like `db:migrate`, `generate model`, `server`
- 🎯 **Convention over Configuration** - Opinionated structure for rapid development
- ⚡ **Async-first** - Built on FastAPI and SQLAlchemy 2.0 async
- 🔋 **Batteries Included** - Auth, admin panel, migrations, and seeding out of the box
- 📦 **Interactive Setup** - Choose your stack (SQLite/PostgreSQL, templates, features)
- 🎨 **Multiple Templates** - Empty, Blog, Chat, SaaS, and more

## Installation

```bash
# Install PyRails
pip install -e .

# Or with uv
uv pip install -e .
```

## Quick Start

```bash
# Create a new app (interactive prompts)
pyrails new myapp

# Navigate to your app
cd myapp

# Generate a model
pyrails generate model Article title:str body:text

# Run migrations
pyrails db:migrate

# Generate a controller
pyrails generate controller Articles

# Start the server
pyrails server
```

Visit:
- http://localhost:8000/docs - API documentation
- http://localhost:8000/admin - Admin panel

## Available Commands

### Generation
- `pyrails new APP_NAME` - Create new app with interactive template selection
- `pyrails generate model NAME field:type...` - Generate model + migration
- `pyrails generate controller NAME [actions...]` - Generate controller
- `pyrails generate test NAME` - Generate test file

### Database
- `pyrails db:create` - Create database tables
- `pyrails db:migrate` - Run migrations
- `pyrails db:seed` - Load seed data
- `pyrails db:reset` - Reset database (destructive!)

### Development
- `pyrails server` - Start development server
- `pyrails console` - Interactive Python REPL with app context
- `pyrails routes` - Display all routes

### Setup
- `pyrails setup stripe` - Configure Stripe API keys
- `pyrails setup openai` - Configure OpenAI API keys

### Deployment
- `pyrails deploy railway` - Deploy to Railway
- `pyrails deploy fly` - Deploy to Fly.io
- `pyrails deploy render` - Deploy to Render

## Templates

Choose from built-in templates when creating a new app:

1. **empty** - Bare structure, no models
2. **blog** - User + Article models with CRUD
3. **chat** - OpenAI-compatible chat with vanilla JS frontend
4. **saas** - Multi-tenant (User + Organization + Stripe)
5. **saas-chat** - Combined SaaS + Chat
6. **api** - API-only, no frontend

## Field Types

When generating models:

- `str` - String(255)
- `text` - Text
- `int` - Integer
- `float` - Float
- `bool` - Boolean
- `datetime` - DateTime
- `date` - Date
- `json` - JSON
- `references` - Foreign key (auto-creates relationships)

## Example

```bash
# Create a blog app
pyrails new myblog

# Choose template: blog
# Choose database: sqlite

cd myblog

# The blog template includes User + Article models
# Generate a controller
pyrails generate controller Articles

# Start the server
pyrails server
```

## Documentation

See [CLAUDE.md](CLAUDE.md) for comprehensive framework documentation.

## License

MIT
