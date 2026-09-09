## Start app
### via docker:
```bash
docker compose up
```
### on local
```bash
uv run uvicorn app.main:app
```
### on local with reload
```bash
uv run uvicorn app.main:app --reload
```

## Development
### adding new dependencies
use uv to install new dependencies
```bash
uv add {new_dep}
```
rebuild docker conteiner after it so it can see the new dependencies
```bash
docker compose up --build
```

### transactions (alembic)
create new revision
```bash
uv run alembic revision --autogenerate -m "{message}"
```
update to the current revision
```bash
alembic upgrade head
```
check current revision
```bash
alembic current
```
