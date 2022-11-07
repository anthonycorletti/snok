#!/bin/sh -ex

mypy python_project_template tests
black python_project_template tests --check
isort python_project_template tests scripts --check-only
ruff python_project_template tests scripts
