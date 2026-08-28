# Scalable Backend & API Platform (Portfolio Sample)

Portfolio demonstration of a production-style backend layout: clear boundaries between HTTP, business logic, and data access â€” with auth, validation, consistent errors, and tests.

> This is a **demo codebase for technical interviews / evaluation calls**, reflecting patterns used in real API work (not a client proprietary system).

## Stack

- Python 3.11+
- FastAPI
- Pydantic v2
- pytest

## Architecture

```
app/
  api/          # HTTP routes only
  services/     # business logic
  repositories/ # data access
  models/       # domain + schemas
  core/         # auth, errors, config
```

## Quick start

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open docs: http://127.0.0.1:8000/docs

## Demo credentials

- Email: `builder@example.com`
- Password: `demo-password`

## Tests

```bash
pytest -q
```

## What to walk through on a call

1. Request flow: route â†’ service â†’ repository
2. Auth + authorization checks
3. Validation and error shape
4. One trade-off (why layered services vs fat routes)
5. Tests covering success + failure paths
