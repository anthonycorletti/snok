# Contributing

Assuming you have cloned this repository to your local machine, you can follow these guidelines to make contributions.

**First, please install pyenv https://github.com/pyenv/pyenv to manage your python environment.**

Use `pyenv install` to install a version of python. You can see the available versions with `pyenv install --list` and the suggested version of python is noted in the `pyproject.toml` file.

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

You should see paths that use the `.venv/bin` in your current working directory.

## Installing dependencies

For your first ever install of `snok` you will need to run;

```sh
pip install -e '.[dev]'
```

From then on, you can use `snok` to build `snok`!

```sh
snok install
```

```sh
snok add pendulum
```

## Linting

```sh
snok lint
```

## Formatting

```sh
snok format
```

## Tests

```sh
snok test
```
