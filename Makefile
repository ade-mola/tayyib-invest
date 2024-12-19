.PHONY: fix
fix:
	poetry run ruff check --preview --fix
	poetry run ruff format

.PHONY: lint
lint:
	poetry run ruff check --preview
	poetry run mypy .