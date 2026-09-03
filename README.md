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