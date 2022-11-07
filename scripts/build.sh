#!/bin/sh -e

pip install --upgrade pip
pip install --upgrade build

python -m build
