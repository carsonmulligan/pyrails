# Architecture

## Design Philosophy

Convention over configuration MVC framework for FastAPI. Inspired by Rails' developer ergonomics while leveraging Python's async ecosystem.

## Core Architecture

### CLI Layer
- Entry: `pyrails.cli:main`
- Click-based command routing with colon notation support (`db:migrate`)
- Rich console output for formatting
- Commands organized by domain (db, admin, generation)

### Generators
Located in `pyrails/generators/`:
- `app_generator.py` - Full application scaffold with interactive prompts
- `model_generator.py` - SQLAlchemy models + Alembic migrations
- `controller_generator.py` - FastAPI routers with RESTful endpoints
- `migration_generator.py` - Standalone migration files

Field type mapping:
```python
{
    'str': 'String(255)',
    'text': 'Text',
    'int': 'Integer',
    'float': 'Float',
    'bool': 'Boolean',
    'datetime': 'DateTime',
    'date': 'Date',
    'json': 'JSON',
    'references': 'ForeignKey with relationship()'
}
```

### Generated App Structure

```
app/
├── models/
│   └── base.py              # Declarative base + Base model
├── controllers/
│   └── __init__.py
└── views/
    └── __init__.py

config/
├── application.py           # FastAPI() instance + router registration
├── database.py              # async_sessionmaker + engine
└── settings.py              # BaseSettings from .env

db/
├── migrations/              # Alembic autogenerate
│   ├── env.py
│   └── versions/
└── seeds/
    └── development.py       # Seed data functions

tests/
└── __init__.py
```

### Database Layer

Async SQLAlchemy 2.0:
- `async_sessionmaker` for connection pooling
- `AsyncSession` context managers
- Type-safe ORM queries with modern syntax

Alembic integration:
- Auto-migration generation from model changes
- Migration runs via `pyrails db:migrate`
- Supports SQLite, PostgreSQL (asyncpg), MySQL (aiomysql)

### Command Implementations

**db:create** - Calls `Base.metadata.create_all()` synchronously
**db:migrate** - Runs `alembic upgrade head`
**db:seed** - Imports and executes `db/seeds/development.py`
**db:reset** - Drop all + recreate + seed (dev only)
**server** - Runs `uvicorn config.application:app --reload`
**console** - IPython REPL with app context loaded

### FastAPI Integration

Generated `config/application.py`:
```python
app = FastAPI()
app.include_router(user_router, prefix="/api")
# Auto-registers controllers from app/controllers/
```

Features:
- Automatic OpenAPI docs at `/docs`
- SQLAdmin mounted at `/admin`
- fastapi-users for auth (optional)
- CORS middleware
- Exception handlers

### Testing

pytest + pytest-asyncio + httpx:
```python
@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

async def test_endpoint(client):
    response = await client.get("/api/posts")
    assert response.status_code == 200
```

## File Generation Templates

Models use Jinja2-like f-strings:
```python
class {model_name}(Base):
    __tablename__ = "{table_name}"
    {fields}
    {relationships}
```

Controllers generate RESTful patterns:
```python
@router.get("/{plural}")
async def list_{plural}(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select({Model}))
    return result.scalars().all()
```

## Inflection

Uses `inflect` library:
- Pluralization: `Post` → `posts`
- Singularization: `articles` → `article`
- Tableize: `BlogPost` → `blog_posts`
- Classify: `blog_posts` → `BlogPost`

## Settings Management

Pydantic BaseSettings with .env:
```python
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    DEBUG: bool = False

    class Config:
        env_file = ".env"
```

## Extension Points

Add custom generators:
1. Create `pyrails/generators/my_generator.py`
2. Implement `MyGenerator.generate()`
3. Register in `cli.py`

Add custom commands:
1. Create `pyrails/commands/my_command.py`
2. Import and register in `cli.py`

## Known Constraints

- Requires Python 3.11+ (modern async syntax)
- SQLite lacks some ALTER TABLE operations (recreate pattern)
- Foreign keys require explicit `references` type
- Controller generator needs manual route registration
- No built-in websocket scaffolding yet

## Performance Considerations

- Async I/O throughout (no blocking calls)
- Connection pooling via async_sessionmaker
- Lazy-loading relationships (use `selectinload` for N+1)
- SQLite: disable in production (concurrency limits)

## Security Defaults

- Generated SECRET_KEY via secrets.token_urlsafe()
- Bcrypt password hashing (passlib)
- CORS disabled by default
- SQL injection protection via parameterized queries
- No raw SQL execution in generators
