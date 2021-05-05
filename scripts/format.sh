#!/bin/sh -ex

# Sort imports one per line, so autoflake can remove unused imports
isort --force-single-line-imports python_project_template tests scripts

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place python_project_template tests scripts --exclude=__init__.py
black python_project_template tests scripts
isort python_project_template tests scripts
