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

You should see paths that use the .venv/bin in your current working directory.

## Installing dependencies

This project uses `pip` to manage our project's dependencies and all tasks are managed with `invoke`. Invoke is a python package that allows you to define tasks in a python file and run them from the command line, similar to `make` and `rake`, but with a pythonic syntax, it's really great!

In your virtual environment, install `invoke` by running;

```sh
pip install --upgrade pip && pip install invoke
```

Then to install the project's dependencies, run;

```sh
inv install
```

## Linting

```sh
inv lint
```

## Formatting

```sh
inv format
```

## Tests

```sh
inv test
```
