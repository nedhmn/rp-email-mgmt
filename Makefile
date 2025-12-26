start:
	uv run python -m rpemail.main

dryrun:
	uv run python -m rpemail.main --dry-run

lint:
	uv run ruff check .

typecheck:
	uv run mypy rpemail

check: lint typecheck

help:
	@echo "start      - Update email signatures for all users"
	@echo "dryrun     - Show signature changes without applying"
	@echo "lint       - Run ruff linter"
	@echo "typecheck  - Run mypy type checker"
	@echo "check      - Run lint + typecheck"
