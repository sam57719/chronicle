## ------------------------------- Builder Stage ------------------------------- ##
FROM ghcr.io/astral-sh/uv:0.11.6-python3.14-trixie-slim AS builder

# Build-time args for reproducibility / overrides
ARG UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=${UV_LINK_MODE} \
    UV_PYTHON_INSTALL_DIR=/python \
    UV_PYTHON_PREFERENCE=only-managed \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# git is required to install the project in editable mode from a bind-mounted .git
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN uv python install

WORKDIR /app

# Copy project metadata first to leverage layer caching for dependency resolution
COPY backend/pyproject.toml backend/uv.lock ./

# Use BuildKit cache for uv sync. Requires BuildKit to be enabled during build.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev --no-editable

# Copy sources
COPY backend/src/ src/

# Install editable project into the uv-managed venv. Mount .git read-only (BuildKit).
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=.git,target=/app/.git,readonly \
    uv pip install --no-deps --editable .

# Remove unnecessary files from the venv and packaged python to reduce image size
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

LABEL org.opencontainers.image.title="menagerist-backend" \
      org.opencontainers.image.source="https://github.com/samcorky/menagerist" \
      org.opencontainers.image.licenses="MIT"

WORKDIR /app

# Copy runtime python, venv and app sources from the builder and set proper ownership
# Copy the installed Python runtime from the builder to /python
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

# Copy healthcheck script and use the full venv python path to avoid PATH brittleness
COPY backend/docker/healthcheck.py /app/healthcheck.py
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["/app/.venv/bin/python", "/app/healthcheck.py"]

# Start granian (the binary will be resolved from the venv via PATH)
CMD ["granian", "--interface", "asgi", "app.entrypoints.api.asgi:app"]
