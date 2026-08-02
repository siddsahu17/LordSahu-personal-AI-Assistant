# Stage 1: Build the Vite production bundle
FROM node:22-alpine AS builder

WORKDIR /app

# Copy package manifests and install dependencies
COPY package*.json ./
RUN npm ci

# Copy frontend source code and build
COPY . .
RUN npm run build

# Stage 2: Serve using Nginx
FROM nginx:alpine

# Copy built dist files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
