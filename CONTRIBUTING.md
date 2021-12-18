# Contributing

Assuming you have cloned this repository to your local machine, you can follow these guidelines to make contributions.

**First, please install pyenv https://github.com/pyenv/pyenv to manage your python environment.**

Install the version of python as mentioned in this repo.

```sh
pyenv install $(cat .python-version)
```

## Use a virtual environment

```sh
python -m venv .venv
```

This will create a directory `.venv` with python binaries and then you will be able to install packages for that isolated environment.

Next, activate the environment.

```sh
source .venv/bin/activate
```

To check that it worked correctly;

```sh
which python pip
```

You should see paths that use the .venv/bin in your current working directory.

## Installing with Flit

This project uses `flit` to manage our project's dependencies.

Install dependencies, including flit.

```sh
./scripts/install.sh
pyenv rehash
```

## Formatting

```sh
./scripts/format.sh
```

## Tests

```sh
./scripts/test.sh
```
