FROM python:3.13-slim AS base

WORKDIR /app

FROM base AS builder

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

RUN pip install --upgrade pip
RUN pip install poetry==2.1.3

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-root

FROM base AS production

COPY --from=builder /app/.venv ./.venv
COPY cloud_app ./cloud_app

RUN useradd app
USER app

CMD [".venv/bin/python", "-m", "uvicorn", "--host", "0.0.0.0", "--port", "8000", "cloud_app.app:app"]
