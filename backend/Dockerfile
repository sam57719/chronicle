## ------------------------------- Builder Stage ------------------------------ ##
FROM python:3.14-bookworm AS builder

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Download the latest installer, install it and then remove it
ADD https://astral.sh/uv/install.sh /install.sh
ENV UV_VERSION=0.9.18
RUN chmod -R 755 /install.sh && /install.sh && rm /install.sh

# Set up the UV environment path correctly
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Copy bare minimum for requirements install
COPY pyproject.toml ./
RUN uv sync --no-install-project --no-install-workspace --no-dev

# Copy the rest of the source code
COPY src/ src/
RUN uv pip install .

## ------------------------------- Production Stage ------------------------------ ##
FROM python:3.14-slim-bookworm AS runtime

# Create a non-root user for security
RUN useradd -m appuser
USER appuser

WORKDIR /app

# Copy the virtual environment and source
COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/src ./src

# Set up environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

# Ensure output is sent straight to terminal without buffering
ENV PYTHONUNBUFFERED=1
ENV UVICORN_HOST="0.0.0.0"
ENV UVICORN_PORT="8000"

# Start the application using uvicorn
CMD ["uvicorn", "app.entrypoints.api.main:app", \
     "--no-server-header", \
     "--proxy-headers", \
     "--forwarded-allow-ips", "127.0.0.1", \
     "--access-log"
     ]
