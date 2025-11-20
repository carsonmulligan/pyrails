# pyrails-mvc

Convention over configuration MVC framework for FastAPI. Rails-inspired CLI and project structure for Python's async ecosystem.

**Install:** `pip install pyrails-mvc`
**Repo:** https://github.com/carsonmulligan/pyrails

## Quick Start

```bash
pyrails new blog
cd blog
pyrails generate model Post title:str body:text
pyrails db:migrate
pyrails server
```

Visit http://localhost:8000/docs for Swagger UI.

## Core Commands

```bash
pyrails new APP              # Create application
pyrails g model NAME [...]   # Generate model + migration
pyrails g controller NAME    # Generate RESTful controller
pyrails db:migrate           # Run migrations
pyrails db:seed             # Load seed data
pyrails server              # Start dev server (hot reload)
pyrails console             # Interactive REPL with app context
pyrails routes              # Show all routes
```

## Stack

- **Web:** FastAPI (async endpoints, OpenAPI docs)
- **ORM:** SQLAlchemy 2.0 (async, type-safe)
- **Migrations:** Alembic
- **Auth:** fastapi-users
- **Admin:** sqladmin
- **Config:** Pydantic Settings

## Field Types

```bash
pyrails g model Article \
  title:str \
  slug:str \
  body:text \
  views:int \
  rating:float \
  published:bool \
  created_at:datetime \
  author:references
```

Supported: `str`, `text`, `int`, `float`, `bool`, `datetime`, `date`, `json`, `references`

## Project Structure

```
app/
├── models/         # SQLAlchemy models
├── controllers/    # FastAPI route controllers
└── views/          # Jinja2 templates
config/
├── application.py  # FastAPI app instance
├── database.py     # Async SQLAlchemy engine
└── settings.py     # Pydantic settings from .env
db/
├── migrations/     # Alembic migrations
└── seeds/          # Seed data
tests/              # pytest suite
.env               # DATABASE_URL, SECRET_KEY, etc.
```

## Database Support

```bash
# SQLite (default)
DATABASE_URL=sqlite+aiosqlite:///./app.db

# PostgreSQL
pip install pyrails-mvc[postgresql]
DATABASE_URL=postgresql+asyncpg://user:pass@host/db

# MySQL
pip install pyrails-mvc[mysql]
DATABASE_URL=mysql+aiomysql://user:pass@host/db
```

## Development

```bash
git clone https://github.com/carsonmulligan/pyrails.git
cd pyrails
pip install -e ".[dev]"
pytest
ruff check pyrails/
```

## License

MIT
