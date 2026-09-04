FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.7.2 /uv /uvx /bin/
WORKDIR /app
COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev
COPY . .
RUN uv sync --frozen --no-dev
ENV ENV="docker"
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0"]
