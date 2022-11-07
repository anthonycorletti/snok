#!/bin/sh -ex

mypy python_project_template_anthony tests
black python_project_template_anthony tests --check
isort python_project_template_anthony tests scripts --check-only
ruff python_project_template_anthony tests scripts
