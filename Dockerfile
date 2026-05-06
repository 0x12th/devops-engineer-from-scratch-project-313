FROM node:22-bookworm AS frontend

WORKDIR /app
COPY package.json ./
RUN npm install
RUN mkdir -p /app/public && cp -r ./node_modules/@hexlet/project-devops-deploy-crud-frontend/dist/. /app/public/

FROM python:3.12-slim AS app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    BACKEND_PORT=8080

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends nginx curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev

COPY . .
COPY --from=frontend /app/public /app/public
COPY .configs/nginx.conf /etc/nginx/nginx.conf.template
COPY .scripts/docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8080

CMD ["/app/docker-entrypoint.sh"]
