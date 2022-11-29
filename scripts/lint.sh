#!/bin/sh -ex

mypy python_project_template tests
black python_project_template tests --check
ruff python_project_template tests scripts
