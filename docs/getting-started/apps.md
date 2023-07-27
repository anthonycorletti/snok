# Packages

Snok is great for scaffolding out initial, un-opinionated structure for your python package.

## Getting ready

First set up your local environment by creating a directory and activating a virtual environment:

Assuming you have python 3.11+ installed:

```sh
mkdir -p mypackage && cd mypackage
python -m venv .venv
source .venv/bin/activate
```

You should see the path to your virtual environment now:

```
$ which python pip
/Users/anthony/Desktop/mypackage/.venv/bin/python
/Users/anthony/Desktop/mypackage/.venv/bin/pip
```

## Installing Snok

Install Snok with pip:

```sh
pip install snok
```

Check that snok was installed:

```sh
snok
```

If you're using pyenv (recommended), you may have to rehash your shims

```sh
pyenv rehash
```

## Creating a new app

Create a new app with:

```sh
snok new myapp --type app
```

## Check that everything's ready to go!

```sh
snok ok
```

## Let's build some stuff!

```sh
...
```
