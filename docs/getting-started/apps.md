# Packages

Snok is great for scaffolding out initial, un-opinionated structure for your python package.

## Getting ready

First set up your local environment by creating a directory and activating a virtual environment:

Assuming you have python 3.11+ installed:

```sh
cd $HOME/Desktop
mkdir -p myapp && cd myapp
python -m venv .venv
source .venv/bin/activate
```

You should see the path to your virtual environment now:

```
$ which python pip
/Users/anthony/Desktop/myapp/.venv/bin/python
/Users/anthony/Desktop/myapp/.venv/bin/pip
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

## Let's build some stuff!

You can generate the following kinds of scaffolding;

- Database Models
- FastAPI APIRouters
- Full CRUD Scaffolding

Let's walk through an example of each.

### Prerequisites

First you'll have to run a database. Snok supports Postgres at the moment and will support other SQL databases in the future.

You will need to have docker installed and running on your machine.

Run the following to make sure docker is running:

```sh
docker ps
```

If that doesn't work you can learn how to install docker [here](https://docs.docker.com/engine/install/).

Once you're all set up you can run a postgres database with:

```sh
docker run --rm --name=postgres -d -p 5432:5432 -e POSTGRES_USER=myapp -e POSTGRES_PASSWORD=myapp -e POSTGRES_HOST_AUTH_METHOD=password -e POSTGRES_DB=myapp postgres:15
```

### Check that everything's ready to go!

```sh
snok ok
```

### Create a Database Model

```sh

```

### Create a FastAPI APIRouters

```sh

```

### Create Full CRUD Scaffolding

```sh

```
