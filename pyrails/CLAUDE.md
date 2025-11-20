# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyRails is a Rails-inspired web framework built on FastAPI that brings Ruby on Rails' developer experience to Python. It provides convention over configuration for FastAPI applications with an async-first design.

**Core Philosophy:**
- Convention over Configuration
- CLI-first developer experience (like `rails` commands)
- Async-native using SQLAlchemy 2.0+ and asyncio
- Batteries included (auth, admin panel, migrations, seeding)

## Project Structure (Target)

The PyRails package itself will be structured as:

```
pyrails/
├── pyrails/                  # Main package
│   ├── cli.py               # Main CLI entry point
│   ├── generators/          # Code generators (model, controller, app)
│   │   ├── app_generator.py
│   │   ├── model_generator.py
│   │   ├── controller_generator.py
│   │   └── templates/       # Jinja2 templates for generation
│   ├── commands/            # CLI commands implementation
│   │   ├── db.py           # db:* commands
│   │   ├── server.py       # server command
│   │   ├── console.py      # console command
│   │   └── admin.py        # admin:* commands
│   └── templates/          # Full app templates for 'pyrails new'
├── tests/                  # Framework tests
├── pyproject.toml         # Package configuration
└── pyrails-spec.md        # Complete framework specification
```

## Generated App Structure

When users run `pyrails new myapp`, it creates:

```
myapp/
├── app/
│   ├── models/          # SQLAlchemy models (one file per model)
│   ├── controllers/     # FastAPI routers (one file per resource)
│   ├── services/        # Business logic layer
│   ├── views/          # Jinja2 templates
│   └── assets/         # Static files (CSS, JS)
├── config/
│   ├── application.py   # Main FastAPI app setup
│   ├── database.py     # Database configuration
│   └── settings.py     # Pydantic settings
├── db/
│   ├── seeds/          # Seed data files (development.py, production.py)
│   └── migrations/     # Alembic migrations
└── tests/              # Application tests
```

## Key CLI Commands

The framework provides Rails-like CLI commands using colon notation (Rails-style):

**Generation:**
- `pyrails new APP_NAME` - Interactive prompt for template, database, features
- `pyrails generate model Article title:str body:text user:references` - Generate model + migration
- `pyrails generate controller Articles index show create update destroy` - Generate controller
- `pyrails generate test User` - Generate test file for existing code

**Database:**
- `pyrails db:create` - Create all database tables from models
- `pyrails db:migrate` - Run Alembic migrations (auto-generated from models)
- `pyrails db:seed` - Load seed data from db/seeds/
- `pyrails db:reset` - Drop, create, migrate, seed (always requires confirmation!)

**Development:**
- `pyrails server` - Start Uvicorn dev server with auto-reload (warns about pending migrations)
- `pyrails console` - Interactive IPython REPL (falls back to standard REPL if IPython not installed)
- `pyrails routes` - Display all registered routes
- `pyrails admin:create EMAIL` - Create superuser account

**Setup & Configuration:**
- `pyrails setup stripe` - Interactive setup for Stripe API keys
- `pyrails setup openai` - Interactive setup for OpenAI API keys
- `pyrails setup` - General configuration wizard

**Deployment:**
- `pyrails deploy railway` - Deploy to Railway (auto-configured)
- `pyrails deploy fly` - Deploy to Fly.io (auto-configured)
- `pyrails deploy render` - Deploy to Render (auto-configured)

## Naming Conventions

The framework enforces strict naming conventions:

**Models:**
- File: `app/models/user.py` (singular)
- Class: `class User`
- Table: `users` (auto-pluralized)
- Timestamps: `created_at`, `updated_at` (auto-added)

**Controllers:**
- File: `app/controllers/users_controller.py` (plural + _controller)
- Router prefix: `/api/users`
- Actions: `index`, `show`, `create`, `update`, `destroy`

**Foreign Keys:**
- Field type: `user:references` generates `user_id = Column(Integer, ForeignKey("users.id"))`
- Auto-creates bidirectional relationships

## Field Types for Generators

When generating models, these field types map to SQLAlchemy columns:
- `str` → `String(255)`
- `text` → `Text`
- `int` → `Integer`
- `float` → `Float`
- `bool` → `Boolean`
- `datetime` → `DateTime`
- `date` → `Date`
- `json` → `JSON`
- `references` → `ForeignKey` (auto-creates relationship)

## Technology Stack

**Core Dependencies:**
- FastAPI 0.115+ - Web framework
- SQLAlchemy 2.0+ - ORM (async)
- Alembic - Database migrations
- Uvicorn - ASGI server
- Pydantic - Settings and validation

**Included Batteries:**
- FastAPI Users - Authentication (JWT, OAuth2)
- SQLAdmin - Auto-generated admin panel
- Jinja2 - Template engine
- Passlib - Password hashing
- Rich - Pretty CLI output

**Database Support:**
- SQLite (default for development, aiosqlite)
- PostgreSQL (asyncpg)
- MySQL (aiomysql)

## Authentication System

Every generated app includes FastAPI Users integration:
- User model inherits from `SQLAlchemyBaseUserTable[int]`
- JWT authentication backend pre-configured
- Auth routes: `/auth/jwt/login`, `/auth/register`
- Dependencies: `current_active_user`, `current_superuser`

## Admin Panel

SQLAdmin is auto-configured for all models:
- Accessible at `/admin`
- ModelView classes in `app/controllers/admin_controller.py`
- Auto-discovery and registration in `config/application.py`

## Async Patterns

All database operations must be async:

```python
# Correct
async def get_users(session: AsyncSession):
    result = await session.execute(select(User))
    return result.scalars().all()

# Incorrect - don't use sync operations
def get_users(session):
    return session.query(User).all()  # ❌ Wrong
```

## Generator Templates

All generators use Jinja2 templates located in `pyrails/generators/templates/`:
- Enables consistent code generation
- Templates should include helpful comments and docstrings
- Type hints required everywhere
- Generated files should be immediately runnable

## Testing Philosophy

- Tests generated separately via `pyrails generate test User`
- Use pytest with pytest-asyncio
- Test database uses in-memory SQLite
- Fixtures in `tests/conftest.py` provide db_session, admin_user, etc.
- Test naming: `test_{model_name}.py` or `test_{controller_name}.py`
- Generated tests include basic CRUD and relationship tests

## Environment Configuration

Uses Pydantic Settings with `.env` file:
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - JWT secret (required)
- `DEBUG` - Debug mode (default: False)
- `CORS_ORIGINS` - Allowed CORS origins (default: ["http://localhost:3000"])

## Development Workflow

1. Create new app: `pyrails new myapp`
2. Generate models: `pyrails generate model Article title:str body:text`
3. Run migrations: `pyrails db:migrate`
4. Generate controllers: `pyrails generate controller Articles`
5. Seed database: `pyrails db:seed`
6. Start server: `pyrails server`
7. Access:
   - API docs: `http://localhost:8000/docs`
   - Admin panel: `http://localhost:8000/admin`

## Implementation Priorities

When building PyRails framework code:

1. **Developer Experience First** - Make it joyful and productive
2. **Smart Defaults** - Zero config for simple apps, full customization available
3. **Convention Detection** - Auto-infer table names, relationships, routes
4. **Helpful Errors** - Actionable error messages with suggested fixes
5. **Type Safety** - Type hints everywhere, leverage Python 3.11+ features
6. **Performance** - Async-first, minimal overhead over raw FastAPI

## What Makes This Different

**vs Django:** Async-first, lighter weight, convention over configuration, auto OpenAPI docs
**vs Flask:** Batteries included, strong conventions, CLI generators, type safety
**vs FastAPI:** Structure and conventions, integrated database/auth/admin, CLI productivity tools

## Current Status

This repository contains the complete specification for PyRails (`pyrails-spec.md`). Implementation of the framework is the next phase. When implementing:

- Start with core CLI framework and `pyrails new` command
- Then add model/controller generators
- Then add database commands
- Progressively build out features per the roadmap in the spec

## Design Principles

1. **Convention Over Configuration** - Strong opinions, sensible defaults
2. **Progressive Disclosure** - Simple things simple, complex things possible
3. **Async All The Way** - Never block the event loop
4. **Type Safety** - Leverage Python's type system fully
5. **Rails-Inspired** - Learn from Rails' 20 years of web framework wisdom
6. **Python-Native** - Don't fight Python's idioms, embrace them

## CLI Design Decisions

These decisions were made to optimize developer experience and align with Rails philosophy:

### Command Style
- **Rails-style colons**: Use `db:migrate` not `db migrate`
- **Detailed output**: Show progress with emojis (🚀, ✅, 🌱, ⚠️) and descriptive messages
- **Auto-install dependencies**: Prompt to install missing packages (e.g., "uvicorn not found. Install? [Y/n]")
- **Always prompt on overwrite**: Ask before replacing existing files to prevent accidents

### Project Creation
- **Interactive template selection**: `pyrails new myapp` prompts for template choice
- **Auto-initialize git**: Create repo and initial commit automatically
- **Prompt order**: Template → Database → Features (logical progression)

### Built-in Templates
1. **empty** - Bare structure, no models
2. **blog** - User + Article models with CRUD
3. **chat** - OpenAI-compatible chat with vanilla JS frontend + WebSockets
4. **saas** - Multi-tenant (User + Organization + Membership + Stripe integration)
5. **saas-chat** - Combines chat + saas templates
6. **api** - API-only, no templates/views, just JSON endpoints

### Database & Package Management
- **Default to SQLite**: Use SQLite for development, PostgreSQL available as option
- **Prefer vanilla JS**: No frontend framework in templates, pure vanilla JavaScript
- **Use uv by default**: Generate `pyproject.toml` + `uv.lock`, but works with pip/conda too
- **ORM-only approach**: Generate SQLAlchemy ORM code only, no SQL Core

### Generator Behavior
- **Auto-generate migrations**: `generate model` creates both model file + Alembic migration
- **Auto-update relationships**: When using `user:references`, update both models with bidirectional relationships
- **Return SQLAlchemy models**: Controllers return ORM models directly, FastAPI serializes automatically
- **Separate test generation**: Use `pyrails generate test User` to create tests on demand

### Development Commands
- **IPython preference**: Use IPython for `console` if installed, fall back to standard REPL
- **Migration warnings**: `server` command warns about pending migrations but doesn't auto-run
- **Confirmation on destructive**: `db:reset` always requires user confirmation (never skip)

### Setup & Configuration
- **Dedicated setup command**: `pyrails setup stripe` guides through API key configuration
- **Write to .env**: Setup commands store keys in `.env` file securely
- **Optional features**: Templates with Stripe/OpenAI include commented code + feature flags

### Custom Templates
- **Project overrides global**: Check `.pyrails/templates/` in project first, then `~/.pyrails/templates/`
- **Ship built-in + allow custom**: Include default templates but support user-created ones
- **Template structure**: Custom templates follow same structure as built-in ones

### Deployment
- **Built-in deploy commands**: `pyrails deploy railway/fly/render` auto-configure and deploy
- **Platform-specific configs**: Generate Dockerfile, railway.json, fly.toml as needed
- **One-command deploy**: Minimize steps from code to production
