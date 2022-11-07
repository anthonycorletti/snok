#!/bin/sh -e

pip install --upgrade pip
pip install --upgrade twine

twine upload dist/*
