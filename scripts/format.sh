#!/bin/sh -ex

black python_project_template_anthony tests scripts
isort python_project_template_anthony tests scripts
ruff python_project_template_anthony tests scripts --fix
