#!/bin/sh -ex

black python_project_template tests scripts
ruff check python_project_template tests scripts --fix
