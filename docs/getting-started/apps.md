# Apps

Snok is great for scaffolding out RESTful APIs with FastAPI.

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

### Run the server!

In one terminal session run:

```sh
snok server
```

And in another terminal session run:

```sh
curl -s -X GET http://127.0.0.1:8000/livez
```

You should see something to the effect of:

```json
{"message":"ok"}
```

Let's stop the server and commit our code to the git repo snok set up for us before moving on to the next step.

### Create a Database Model

Let's create a database model for a blog post.

```sh
snok generate model post title:str body:str
```

Snok created a new file in `myapp/models/post.py` that looks like this:

```python
from myapp.kit.db import RecordModel


class Posts(RecordModel, table=True):
    __tablename__ = "posts"

    title: str
    body: str
```

It also added the import statement to `myapp/models/__init__.py`.

Let's run the migrations to create the table in our database.

Make sure the development db is set up

```
PGPASSWORD=myapp psql -h 0.0.0.0 -U myapp -c "create database myapp_development owner myapp;"
```

And run the migrations:

```sh
snok db revision -a -m "posts"
snok db migrate
```

Now let's check that the table was created:

```sh
$ PGPASSWORD=myapp psql -h 0.0.0.0 -U myapp -d myapp_development -c "\d posts"
                           Table "public.posts"
   Column   |            Type             | Collation | Nullable | Default
------------+-----------------------------+-----------+----------+---------
 created_at | timestamp without time zone |           | not null |
 updated_at | timestamp without time zone |           | not null |
 deleted_at | timestamp without time zone |           |          |
 id         | uuid                        |           | not null |
 title      | character varying           |           | not null |
 body       | character varying           |           | not null |
Indexes:
    "pk_posts" PRIMARY KEY, btree (id)
    "ix_posts_id" btree (id)
```

Wow! That's cool! Let's commit our code to git again and move on to the next part.

If you run into any pre-commit snags, you can run `snok format` to format your code. Snok uses `ruff` under the hood to format your code, so you can run `ruff` directly if you want to as well.

### Create FastAPI APIRouters

Creating routers is fairly straightforward.

```sh
snok g router myrouter hello world
```

Now run the server again and check out the new endpoint:

```sh
snok server
```

If you go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser you should see the new endpoints!

Fill those in however you like.

Commit your code again and let's move on to our last example for now.

### Create Full CRUD Scaffolding

Now for the fun part!

Let's create a full CRUD scaffold for an "authors" entity.

```sh
snok g scaffold author name:str age:int
```

Wow! This created a bunch of files

```
$ git status -sb -u
## main
 M myapp/models/__init__.py
 M myapp/router.py
?? myapp/authors/__init__.py
?? myapp/authors/router.py
?? myapp/authors/schemas.py
?? myapp/authors/service.py
?? myapp/models/authors.py
?? tests/authors/__init__.py
?? tests/authors/test_router.py
```

This generated tests for the router and service, as well as the router, service, and model files themselves.

Let's test this code out!

```sh
snok test
```

Awesome! We just generated a fully tested CRUD feature with tests super fast!

Let's run our migrations.

```sh
snok db revision -a -m "authors"
snok db migrate
```

Let's check the table

```sh
$ PGPASSWORD=myapp psql -h 0.0.0.0 -U myapp -d myapp_development -c "\d authors"
                          Table "public.authors"
   Column   |            Type             | Collation | Nullable | Default
------------+-----------------------------+-----------+----------+---------
 created_at | timestamp without time zone |           | not null |
 updated_at | timestamp without time zone |           | not null |
 deleted_at | timestamp without time zone |           |          |
 id         | uuid                        |           | not null |
 name       | character varying           |           | not null |
 age        | integer                     |           | not null |
Indexes:
    "pk_authors" PRIMARY KEY, btree (id)
    "ix_authors_id" btree (id)
```

Let's run the server again and check out the new endpoints:

```sh
snok server
```

List authors

```sh
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v0/authors?order_by=updated_at&order_direction=desc&offset=0&limit=10' \
  -H 'accept: application/json'
```

Create an author

```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v0/authors' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "anthony",
  "age": 42
}'
```

Grab the ID of the author you just created and update it

```sh
ID=$(curl -s -X 'GET' 'http://127.0.0.1:8000/api/v0/authors?order_by=updated_at&order_direction=desc&offset=0&limit=10' -H 'accept: application/json' | jq -r '.[0] | .id')

curl -X 'PUT' \
  http://127.0.0.1:8000/api/v0/authors/${ID} \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "anthony",
  "age": 24
}'
```

Now delete the user you just created 😭

```sh
curl -X 'DELETE' \
  http://127.0.0.1:8000/api/v0/authors/${ID} \
  -H 'accept: */*'
```

You shouldn't be able to find the user anymore

```sh
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v0/authors?order_by=updated_at&order_direction=desc&offset=0&limit=10' \
  -H 'accept: application/json'
```

Super cool! Let's commit our code again and revel in our glory! We just made a full CRUD feature in a few minutes!
