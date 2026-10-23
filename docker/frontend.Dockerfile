# Build with context course-app/frontend; use the upstream lockfile and source.
FROM node:22 AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY . .
ARG VITE_API_URL=
ENV NODE_OPTIONS=--max-old-space-size=768
RUN npm run build

FROM nginxinc/nginx-unprivileged:1.30-alpine
# Preserve the upstream SPA routing and its existing backend fallback config.
COPY --from=build /app/dist/ /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf
USER root
RUN apk upgrade --no-cache \
    && apk add --no-cache --upgrade nginx \
    && sed -i 's/listen 80;/listen 8080;/' /etc/nginx/conf.d/default.conf
USER 101:101
EXPOSE 8080
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 CMD wget -q -O /dev/null http://127.0.0.1:8080/
