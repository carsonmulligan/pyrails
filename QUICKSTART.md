# PyRails Quick Start

## Install

```bash
git clone https://github.com/yourusername/pyrails.git
cd pyrails
pip install -e .
```

## Create Your First App

```bash
# Create app (interactive)
pyrails new blog

# Enter choices:
# Template: 2 (blog)
# Database: 1 (sqlite)
# Git: y
# Dependencies: n (for now)

cd blog
```

## Generated Structure

```
blog/
├── app/
│   ├── models/base.py
│   ├── controllers/
│   └── views/
├── config/
│   ├── application.py  # FastAPI app
│   ├── database.py     # Async SQLAlchemy
│   └── settings.py     # Pydantic settings
└── .env               # DATABASE_URL, SECRET_KEY
```

## Generate Code

```bash
# Model with fields
pyrails generate model Post title:str body:text published:bool

# With foreign key
pyrails generate model Comment post:references body:text

# Controller
pyrails generate controller Posts

# Tests
pyrails generate test Post
```

## Database

```bash
pyrails db:create   # Create tables
pyrails db:migrate  # Run migrations
pyrails db:seed     # Load seed data
```

## Run

```bash
pyrails server
# Visit http://localhost:8000/docs
```

## Development

```bash
pyrails console  # REPL with app loaded
pyrails routes   # Show all routes
```

## Field Types

- `str` - String(255)
- `text` - Text (no limit)
- `int` - Integer
- `float` - Float
- `bool` - Boolean
- `datetime` - DateTime
- `references` - Foreign key

## Common Patterns

### API Endpoint
```bash
pyrails g model Article title:str body:text
pyrails g controller Articles
pyrails server
# GET /api/articles
```

### With Relationships
```bash
pyrails g model Author name:str email:str
pyrails g model Book title:str author:references
# Auto-creates bidirectional relationship
```

### Full Stack
```bash
pyrails new myapp
cd myapp
pyrails g model User email:str
pyrails g controller Users
pyrails db:create
pyrails server
```

## Testing Your Installation

```bash
cd /tmp
pyrails new testapp <<< "1\n1\ny\nn"
cd testapp
pyrails g model Article title:str
ls -la app/models/  # Should see article.py
```

## Next Steps

- Read [CONTRIBUTING.md](CONTRIBUTING.md) for development
- Check [CLAUDE.md](CLAUDE.md) for architecture
- Run `make test` to verify install
- Run `make demo` to create demo app
