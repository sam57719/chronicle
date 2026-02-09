## ------------------------------- Builder Stage ------------------------------- ##
FROM node:20-alpine AS build
WORKDIR /app

# Copy package files first for caching
COPY package.json package-lock.json ./

# Install dependencies (reproducible, CI-friendly)
RUN npm ci --legacy-peer-deps

# Copy source code
COPY . .

# Build the SvelteKit app (outputs to 'build')
RUN npm run build


## ------------------------------- Runtime Stage ------------------------------- ##
FROM ghcr.io/nginx/nginx-unprivileged:alpine-slim

WORKDIR /usr/share/nginx/html

# Copy the static build from builder
COPY --from=build /app/build /usr/share/nginx/html

# Copy Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port
EXPOSE 80

# Healthcheck
HEALTHCHECK --interval=60s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://0.0.0.0:80/ || exit 1

# Run Nginx in foreground (non-root)
CMD ["nginx", "-g", "daemon off;"]
