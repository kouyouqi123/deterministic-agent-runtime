.PHONY: install test lint typecheck check clean

install:
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check .

typecheck:
	mypy .

check: lint typecheck test

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
