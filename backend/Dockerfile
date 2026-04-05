## ------------------------------- Builder Stage ------------------------------- ##
FROM ghcr.io/astral-sh/uv:0.9.25-python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_INSTALL_DIR=/python \
    UV_PYTHON_PREFERENCE=only-managed \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN uv python install

WORKDIR /app

# Copy entire workspace structure — uv needs it to resolve members
COPY pyproject.toml uv.lock ./
COPY backend/ ./backend/
COPY versioning/ ./versioning/

# Install all workspace dependencies and project
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=.git,target=/app/.git \
    uv sync --frozen --no-dev --no-editable --package menagerist

# Cleanup
RUN find /app/.venv -type d -name "__pycache__" -exec rm -rf {} + \
    && find /app/.venv -type d -name "tests" -exec rm -rf {} + \
    && find /app/.venv -name "*.pyi" -delete \
    && find /app/.venv -name "*.pyx" -delete \
    && rm -rf \
       /python/lib/python3.14/test \
       /python/lib/python3.14/ensurepip \
       /python/lib/python3.14/idle* \
       /python/lib/python3.14/tkinter \
       /python/lib/python3.14/site-packages/pip


## ------------------------------- Runtime Stage ------------------------------- ##
FROM gcr.io/distroless/cc-debian13

WORKDIR /app

COPY --from=builder --chown=nonroot:nonroot /python /python
COPY --from=builder --chown=nonroot:nonroot /app/.venv /app/.venv
COPY --from=builder --chown=nonroot:nonroot /app/backend/src /app/src
COPY --from=builder --chown=nonroot:nonroot /app/backend/pyproject.toml /app/backend/

USER nonroot:nonroot

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    GRANIAN_HOST="0.0.0.0" \
    GRANIAN_PORT="8000" \
    GRANIAN_LOG_ACCESS_ENABLED="true" \
    GRANIAN_LOG_LEVEL="info"

EXPOSE 8000

COPY backend/docker/healthcheck.py /app/healthcheck.py
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "/app/healthcheck.py"]

CMD ["granian", "--interface", "asgi", "app.entrypoints.api.asgi:app"]
