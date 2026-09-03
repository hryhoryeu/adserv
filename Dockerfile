FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
RUN uv sync --frozen --no-install-project
COPY . /app
RUN uv sync --frozen
CMD ["uv", "run", "uvicorn", "app.main:app"]