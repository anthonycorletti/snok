#!/bin/sh -e

pip install --upgrade pip
pip install --no-cache-dir '.[dev,test]'

pre-commit install
pre-commit autoupdate
