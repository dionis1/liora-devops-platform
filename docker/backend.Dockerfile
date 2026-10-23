# Build with context course-app/backend after scripts/prepare-course-app.sh.
# Build and runtime must share musl; a Debian-built venv cannot run on Alpine.
FROM python:3.12.15-alpine3.24@sha256:b658b05ce9c4eb97ec6fc19424818a1f31993659c2b505a532f470e83807815d AS base
RUN apk upgrade --no-cache \
    && apk add --no-cache bash \
    && addgroup -g 10001 app \
    && adduser -D -u 10001 -G app app

FROM base AS build
COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /bin/uv
WORKDIR /app
ENV UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev --no-install-project
COPY scripts ./scripts
COPY alembic.ini ./
COPY app ./app
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev

FROM base AS runtime
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/app PATH=/app/.venv/bin:$PATH
WORKDIR /app
COPY --from=build --chown=10001:10001 /app /app
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=3s --start-period=15s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/utils/health-check/', timeout=2)"
CMD ["uvicorn", "app.platform_metrics:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
