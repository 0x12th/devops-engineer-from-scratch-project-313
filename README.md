# URL Shortener

Flask-приложение для сокращения ссылок.

[![Actions Status](https://github.com/0x12th/devops-engineer-from-scratch-project-313/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/0x12th/devops-engineer-from-scratch-project-313/actions)
[![tests](https://github.com/0x12th/devops-engineer-from-scratch-project-313/actions/workflows/tests.yml/badge.svg)](https://github.com/0x12th/devops-engineer-from-scratch-project-313/actions/workflows/tests.yml)

## Environment

```bash
DATABASE_URL=postgres://postgres:password@localhost:5432/appdb
BASE_URL=http://localhost:8080
PORT=8080
BACKEND_PORT=8080
```

## Install

```bash
make install
```

```bash
make setup
```

## Run

```bash
make run
```

Backend: `http://localhost:8080`
Frontend: `http://localhost:5173`

## Checks

```bash
make lint
make test
make pre-commit
```

## Docker

```bash
docker build -t url-shortener .
docker run --rm -p 8080:8080 \
  -e PORT=8080 \
  -e DATABASE_URL='postgres://postgres:password@host.docker.internal:5432/appdb' \
  -e BASE_URL='http://localhost:8080' \
  url-shortener
```
