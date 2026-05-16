PORT ?= 8080
FRAMEWORK ?= flask

.PHONY: setup install install-hooks run run-backend run-frontend lint pre-commit

install:
	uv sync
	npm install

install-hooks:
	uv run pre-commit install

run:
	npx concurrently "make run-backend" "make run-frontend"

run-backend:
	PORT=$(PORT) uv run flask --app app.main:app run --host 0.0.0.0 --port $(PORT)

run-frontend:
	npx start-hexlet-devops-deploy-crud-frontend

lint:
	uv run ruff check .

pre-commit:
	uv run pre-commit run --all-files
