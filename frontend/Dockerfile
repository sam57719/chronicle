# Stage 1: Build the Svelte 5 app
FROM node:20-alpine AS build
WORKDIR /app

# Copy lockfile along with package.json for better cache invalidation strategy
COPY package.json package-lock.json ./

# Use 'npm ci' for faster, reproducible installs in automated environments.
# It skips the dependency resolution tree and uses the lockfile exactly.
RUN npm ci --legacy-peer-deps

# Copy the rest of the frontend code
COPY . .

# Run the SvelteKit build (outputs to the 'build' folder)
RUN npm run build

# Stage 2: Serve the static files with Nginx
FROM nginx:alpine-slim

# Copy the static output from the build stage to Nginx's serve directory
# Note: SvelteKit with adapter-static defaults to the 'build' directory
COPY --from=build /app/build /usr/share/nginx/html

# Copy your custom Nginx configuration for the API proxy
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://0.0.0.0:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
