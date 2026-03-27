.PHONY: install dev lint fmt test clean

install:
	uv pip install -e .

dev:
	uv pip install -e ".[dev,bigquery]"

lint:
	ruff check drt tests
	mypy drt

fmt:
	ruff format drt tests
	ruff check --fix drt tests

test:
	pytest

clean:
	rm -rf dist build .eggs *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
