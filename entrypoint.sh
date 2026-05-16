#!/bin/sh
set -e

: "${PORT:=80}"
: "${BACKEND_PORT:=8080}"

sed -i "s/listen 80;/listen ${PORT};/" /etc/nginx/conf.d/default.conf

BACKEND_PORT="${BACKEND_PORT}" python -m app.main &
exec nginx -g "daemon off;"
