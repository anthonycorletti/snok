#!/bin/sh -e

pip install --upgrade pip
pip install --no-cache-dir -e '.[dev,test]'

pre-commit install
pre-commit autoupdate
