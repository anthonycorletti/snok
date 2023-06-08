# Contributing

Assuming you have cloned this repository to your local machine, you can follow these guidelines to make contributions.

**First, please install pyenv https://github.com/pyenv/pyenv to manage your python environment.**

Install a version of python that matches the version requirement in this repository's `pyproject.toml`.

```sh
pyenv install <PYTHON-VERSION>
```

## Create your virtual environment

```sh
python -m venv .venv
```

This will create a directory `.venv` with python binaries and then you will be able to install packages for that isolated environment. You can replace `.venv` with any directory name you want.

Next, activate the environment.

```sh
source .venv/bin/activate
```

To check that it worked correctly;

```sh
which python pip
```

You should see paths that use `.venv/bin` in your current working directory.

## Dependencies

This project uses `invoke` to manage dependencies.

In your virtual environment, install `invoke` by running;

```sh
pip install --upgrade pip && pip install invoke
```

Then to install the project's dependencies, run;

```sh
inv install
```

To add a specific dependency, run;

```sh
inv add <PACKAGE>
```

To remove a specific dependency, run;

```sh
inv rm <PACKAGE>
```

## Tasks

All tasks are managed with `invoke`.

Invoke is a python package that allows you to define tasks in a python file and run them from the command line, similar to `make` and `rake`, but with a pythonic syntax. All tasks are located in the `tasks.py` file.

### Linting

```sh
inv lint
```

### Formatting

```sh
inv format
```

### Tests

```sh
inv test
```
