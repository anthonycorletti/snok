# Modal

Let's create a snok app and deploy it to modal.

Once it's deployed, we'll check out a few of the infrastructure features that modal provides.

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

### Check that everything's ready to go!

```sh
snok ok
```

## Sign up for Modal

Sign up for Modal and create your account at [https://modal.com](https://modal.com).

## Let's build some stuff!

Now that you have your account all set up, let's build some stuff!

We're going to review three important architectural concepts that we get out of the box with Modal;

1. Key-Value Caching
1. Job Queues
1. Workers

### Authenticate with Modal


### Deploying to Modal

```sh
snok deploy
```

### Key-Value Caching

### Queueing Jobs

### Workers
