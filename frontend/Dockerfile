# Stage 1: Build the Svelte 5 app
FROM node:20-alpine AS build
WORKDIR /app

# Copy package files first to leverage Docker layer caching
COPY package*.json ./

# Install dependencies. Using --legacy-peer-deps helps avoid
# the ERESOLVE issues common with Svelte 5's current ecosystem.
RUN npm install --legacy-peer-deps

# Copy the rest of the frontend code
COPY . .

# Run the SvelteKit build (outputs to the 'build' folder)
RUN npm run build

# Stage 2: Serve the static files with Nginx
FROM nginx:alpine

# Copy the static output from the build stage to Nginx's serve directory
# Note: SvelteKit with adapter-static defaults to the 'build' directory
COPY --from=build /app/build /usr/share/nginx/html

# Copy your custom Nginx configuration for the API proxy
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
