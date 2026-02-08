## ------------------------------- Builder Stage ------------------------------ ##
FROM ghcr.io/astral-sh/uv:0.9.25-python3.14-bookworm-slim AS builder

WORKDIR /app

# Copy bare minimum for requirements install
COPY pyproject.toml ./
RUN uv sync --no-install-project --no-install-workspace --no-dev

# Copy the rest of the source code
COPY src/ src/
RUN uv pip install .

## ------------------------------- Production Stage ------------------------------ ##
FROM python:3.14-slim-bookworm AS runtime

# Create a non-root user to run the application
RUN useradd app
USER app

WORKDIR /app

# Copy the virtual environment and source
COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/src ./src

# Set up environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

COPY docker/healthcheck.py ./healthcheck.py
HEALTHCHECK --interval=60s --timeout=5s --start-period=8s --retries=3 \
 CMD ["python", "/app/healthcheck.py"]

# Ensure output is sent straight to terminal without buffering
ENV PYTHONUNBUFFERED=1

# Prevent Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1

# Set environment variables for granian
ENV GRANIAN_HOST="0.0.0.0"
ENV GRANIAN_PORT="8000"
ENV GRANIAN_LOG_ACCESS_ENABLED=true

# Start the application using granian (ASGI)
CMD ["granian", "--interface", "asgi", "app.entrypoints.api.main:app"]
