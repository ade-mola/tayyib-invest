.PHONY: fix
fix:
	poetry run ruff format
	poetry run ruff check --preview --fix

.PHONY: lint
lint:
	poetry run ruff check --preview
	poetry run mypy .