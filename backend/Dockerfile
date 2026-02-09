## ------------------------------- Builder Stage ------------------------------- ##
FROM ghcr.io/astral-sh/uv:0.9.25-python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_INSTALL_DIR=/python \
    UV_PYTHON_PREFERENCE=only-managed

# Install Python early
RUN uv python install

WORKDIR /app

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev --no-editable --no-install-workspace

# Install project
COPY src/ src/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install . --compile

# Cleanup venv and Python stdlib
RUN find /app/.venv -type d -name "__pycache__" -exec rm -rf {} + \
    && find /app/.venv -type d -name "tests" -exec rm -rf {} + \
    && rm -rf /python/lib/python3.14/test /python/lib/python3.14/ensurepip \
       /python/lib/python3.14/site-packages/pip/_vendor/tests


## ------------------------------- Runtime Stage ------------------------------- ##
FROM gcr.io/distroless/cc

WORKDIR /app

# Switch to non-root user
USER nonroot:nonroot

# Copy Python, venv, source, metadata
COPY --from=builder --chown=nonroot:nonroot /python /python
COPY --from=builder --chown=nonroot:nonroot /app/.venv /app/.venv
COPY --from=builder --chown=nonroot:nonroot /app/src /app/src
COPY --from=builder --chown=nonroot:nonroot /app/pyproject.toml /app/
COPY --from=builder --chown=nonroot:nonroot /app/uv.lock /app/

# Environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV GRANIAN_HOST="0.0.0.0"
ENV GRANIAN_PORT="8000"
ENV GRANIAN_LOG_ACCESS_ENABLED=true
ENV GRANIAN_LOG_LEVEL=debug

# Healthcheck
COPY docker/healthcheck.py /app/healthcheck.py
HEALTHCHECK --interval=60s --timeout=5s --start-period=10s --retries=3 \
  CMD ["python", "/app/healthcheck.py"]

# Run Granian ASGI
CMD ["granian", "--interface", "asgi", "app.entrypoints.api.asgi:app"]
