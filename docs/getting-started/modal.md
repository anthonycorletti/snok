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

Follow the instructions [here](https://modal.com/home).

### Deploying to Modal

Create an `.env.prod` for your production environment:

```sh
cat <<EOF > .env.prod
ENV=prod
API_SECRET_KEY=supersecret
LOG_LEVEL=info
APP_URL=http://127.0.0.1:8000
EOF
```

```sh
snok deploy
```

This should only take a few seconds.

Once deployed, go to [https://modal.com/apps](https://modal.com/apps), find your app under "myapp", and open the url for the app in your browser.

### Key-Value Caching

First let's check out the key-value store.

```sh
curl -X 'GET' \
  YOUR_MODAL_URL/api/v0/cache \
  -H 'accept: application/json'
```

In the logs for you app, you'll see something like:

```
{"event": "Cache.get: key (test) not found", "level": "error", "timestamp": "2023-07-28T03:36:14.153778Z"}
{"event": "get: None", "level": "info", "timestamp": "2023-07-28T03:36:14.154186Z"}
{"event": "contains: False", "level": "info", "timestamp": "2023-07-28T03:36:14.176485Z"}
{"event": "get: toast", "level": "info", "timestamp": "2023-07-28T03:36:14.238603Z"}
{"event": "contains: True", "level": "info", "timestamp": "2023-07-28T03:36:14.258604Z"}
{"event": "Cache.get: key (test) not found", "level": "error", "timestamp": "2023-07-28T03:36:14.299118Z"}
{"event": "get: None", "level": "info", "timestamp": "2023-07-28T03:36:14.299416Z"}
{"event": "contains: False", "level": "info", "timestamp": "2023-07-28T03:36:14.322885Z"}
{"event": "popping again...", "level": "info", "timestamp": "2023-07-28T03:36:14.323222Z"}
{"event": "Cache.pop: key (test) not found", "level": "error", "timestamp": "2023-07-28T03:36:14.343409Z"}
```

Super cool right! With just a few lines of code, we have a key-value store that we can use to cache data.

### Queueing Jobs

Now let's check out the job queue.

```sh
curl -X 'GET' \
  YOUR_MODAL_URL/api/v0/queue \
  -H 'accept: application/json'
```

Your output in the logs should look something like

```
{"event": "get: None", "level": "info", "timestamp": "2023-07-28T03:39:11.445028Z"}
{"event": "get: test", "level": "info", "timestamp": "2023-07-28T03:39:11.505837Z"}
{"event": "get: ['test', 'toast']", "level": "info", "timestamp": "2023-07-28T03:39:11.555796Z"}
{"event": "get: ['test', 'toast']", "level": "info", "timestamp": "2023-07-28T03:39:11.614384Z"}
```

Again, with zero configuration, we have a job queue that we can use to queue up work.

So where would we pull data off the queue and do work?

Glad you asked! That's where workers come in 👇

### Workers

Snok comes configured with some code that allows your to run workers that can run as background jobs if you like. These workers can be configured to run on a schedule, or to run continuously.

If you check out `_modal.py` in your app, you'll see some code that looks like this:

```python
@stub.function(
    image=image,
    secret=stub["env"],
)
async def _run(func: Callable, *args: Any, **kwargs: Any) -> None:
    await func(*args, **kwargs)
```

All that's needed to run a worker is to decorate a function with `@stub.function` and then call that function with the arguments you want to pass to it. This means you can add workers to your app without having to worry about configuring a worker process, or a scheduler, drivers for GPUs, or anything of that sort.

So let's give it a go.

```sh
curl -X 'GET' \
  YOUR_MODAL_URL/api/v0/worker?backgrounded=false \
  -H 'accept: application/json'
```

And in your logs you'll see logs from the outer and inner functions all in order

```
{"event": "running things", "level": "info", "timestamp": "2023-07-28T03:45:35.679145Z"}
{"event": "doing things", "level": "info", "timestamp": "2023-07-28T03:45:38.557821Z"}
{"event": "done doing things", "level": "info", "timestamp": "2023-07-28T03:46:08.558325Z"}
{"event": "done running things", "level": "info", "timestamp": "2023-07-28T03:46:08.601150Z"}
```

Now if you flip the `backgrounded` flag to `true` and run the same command, you'll see that the request returns  immediately, and the work is done in the background.

```
{"event": "running things", "level": "info", "timestamp": "2023-07-28T03:48:45.605908Z"}
{"event": "done running things", "level": "info", "timestamp": "2023-07-28T03:48:45.705178Z"}
Request finished with status 200. (execution time: 104.6 ms, total latency: 2268.1 ms)
{"event": "doing things", "level": "info", "timestamp": "2023-07-28T03:48:48.229605Z"}
{"event": "done doing things", "level": "info", "timestamp": "2023-07-28T03:49:18.230135Z"}
```

For more about functions on modal, check out the [docs](https://modal.com/docs), [guides](https://modal.com/docs/guide), and [examples](https://github.com/modal-labs/modal-examples).

- [Functions](https://modal.com/docs/reference/modal.Function)
- [Functions with Periods](https://modal.com/docs/reference/modal.Period) or [Cron Jobs](https://modal.com/docs/reference/modal.Cron)
