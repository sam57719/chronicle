## ------------------------------- Builder Stage ------------------------------- ##
FROM ghcr.io/astral-sh/uv:0.9.25-python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=hardlink \
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

COPY backend/pyproject.toml backend/uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev --no-editable

COPY backend/src/ src/

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=.git,target=/app/.git \
    uv pip install --no-deps --editable .

RUN find /app/.venv -type d -name "__pycache__" -exec rm -rf {} + \
    && find /app/.venv -type d -name "tests" -exec rm -rf {} + \
    && find /app/.venv -name "*.pyi" -delete \
    && find /app/.venv -name "*.pyx" -delete \
    && find /app/.venv -name "*.a" -delete \
    && find /app/.venv -name "*.so.debug" -delete \
    && find /app/.venv -type d -name "*.dist-info" ! -name "menagerist-*.dist-info" -exec rm -rf {} + \
    && rm -rf \
       /python/lib/python3.14/test \
       /python/lib/python3.14/ensurepip \
       /python/lib/python3.14/idle* \
       /python/lib/python3.14/tkinter \
       /python/lib/python3.14/lib2to3 \
       /python/lib/python3.14/site-packages/pip \
       /root/.cache


## ------------------------------- Runtime Stage ------------------------------- ##
FROM gcr.io/distroless/cc-debian13 AS runtime

WORKDIR /app

COPY --from=builder --chown=nonroot:nonroot /python /python
COPY --from=builder --chown=nonroot:nonroot /app/.venv /app/.venv
COPY --from=builder --chown=nonroot:nonroot /app/src /app/src
COPY --from=builder --chown=nonroot:nonroot /app/pyproject.toml /app/

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
