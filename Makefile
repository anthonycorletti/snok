.DEFAULT_GOAL := all
sources = python_project_template tests

.PHONY: clean
clean:
	rm -rf build dist *.egg-info .pytest_cache .mypy_cache .coverage htmlcov .ruff_cache coverage.xml

.PHONY: install
install:
	pip install --upgrade pip
	pip install --no-cache-dir -e '.[dev,test]'
	pre-commit install
	pre-commit autoupdate
	if command -v pyenv 1>/dev/null 2>&1; then pyenv rehash; fi

.PHONY: lint
lint:
	mypy $(sources)
	black $(sources) --check
	ruff $(sources)

.PHONY: format
format:
	black $(sources)
	ruff $(sources) --fix

.PHONY: test
test:
	pytest -o console_output_style=progress --disable-warnings --cov=python_project_template --cov=tests --cov-report=term-missing --cov-report=xml --cov-report=html --cov-fail-under=100

.PHONY: build
build:
	pip install --upgrade build
	python -m build

.PHONY: publish
publish:
	pip install --upgrade twine
	twine upload dist/*

.PHONY: all
all: clean install format lint test
