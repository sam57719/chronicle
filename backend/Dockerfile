FROM python:3.14.2-bookworm AS builder

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Download the latest installer, install it and then remove it
ADD https://astral.sh/uv/install.sh /install.sh
ENV UV_VERSION=0.9.17
RUN chmod -R 755 /install.sh && /install.sh && rm /install.sh

# Set up the UV environment path correctly
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /backend

COPY pyproject.toml README.md ./

RUN uv sync --no-dev --no-cache --no-interaction

FROM python:3.14.2-slim-bookworm AS runtime

WORKDIR /backend

COPY --from=builder /backend/.venv ./.venv
COPY --from=builder /backend/pyproject.toml ./pyproject.toml
COPY . .

RUN useradd --create-home --shell /bin/bash app

USER app

ENV PATH="/backend/.venv/bin:${PATH}"

EXPOSE 8000

CMD ["./docker/startup.sh"]
