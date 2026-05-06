#!/usr/bin/env sh
set -eu

BACKEND_PORT="${BACKEND_PORT:-8080}"
PORT="${PORT:-8080}"

sed \
  -e "s/__BACKEND_PORT__/${BACKEND_PORT}/g" \
  -e "s/__PORT__/${PORT}/g" \
  /etc/nginx/nginx.conf.template > /tmp/nginx.conf

/app/.venv/bin/gunicorn --bind "127.0.0.1:${BACKEND_PORT}" app.main:app &
nginx -c /tmp/nginx.conf -g "daemon off;"
