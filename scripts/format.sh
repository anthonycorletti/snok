#!/bin/sh -ex

black python_project_template tests scripts
isort python_project_template tests scripts
ruff python_project_template tests scripts --fix
