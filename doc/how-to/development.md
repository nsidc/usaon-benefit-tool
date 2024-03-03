---
title: "Development"
---

## Quickstart

Install [Docker](https://docs.docker.com/engine/install/) and
[Docker Compose](https://docs.docker.com/compose/install/).

```bash
ln -s compose.dev.yml compose.override.yml
docker compose up -d

# IMPORTANT: First time only. Initializing DB starts fresh, deleting all entered data:
./scripts/invoke_in_container.sh db.init
```

This will provide a hot-reloading dev server. Use `docker compose logs -f` to watch the
logs.


## The details

It's easiest to work with and support Docker Compose here. Many other workflows are
great options, but they are not in scope for this documentation.


### Install Docker Compose

Install [Docker](https://docs.docker.com/engine/install/) and
[Docker Compose](https://docs.docker.com/compose/install/).

Docker Desktop provides both of these. There are alternatives, like Podman, but they are
not in scope for this documentation.


### Symlink dev Compose config

Create a symbolic link to the dev Compose config with a magical name.
`compose.override.yml`, if present is merged on top of `compose.yml`. This gives us a
dev server instead of a production server, and other conveniences.

```bash
ln -s compose.dev.yml compose.override.yml
```


### Environment variables

Our development Compose file does not require any of
[our application's environment variables](/reference/envvars.md), but if you want to
test with Google SSO or with a remote database, you may want to uncomment some lines in
`compose.dev.yml`.

:::{.callout-note}
Envvar values can be persisted in a `.env` file so they are passed to containers
automatically by Docker Compose. This file is part of `.gitignore` so that no secrets
are committed to github.
:::

:::{.callout-warning}
**Never put secret** (or non-constant!) **environment variables in Compose YAML,
because that makes it easy to accidentally expose those to the internet.**
:::


### Start the service

Bring up the docker container:

```bash
docker compose up -d
```

**The stack should now be up, with the web interface running at `locahost:5000`, and
database administration at `localhost:8080`.**

You can follow the logs with:

```bash
docker compose logs -f
```


### Initialize the database

:::{.callout-note}
In dev this will initialize a PostgreSQL DB that is preserved in the `_db/` directory.
In NSIDC deployment environments we deploy the db on a separate host using the
[usaon-benefit-tool-db project](https://github.com/nsidc/usaon-benefit-tool-db).

**The dev credentials are specified in `compose.dev.yml`.**
:::

Run `./scripts/invoke_in_container.sh db.init`

This can also be used to drop and recreate all the tables, for example, after a model
change.

:::{.callout-warning}
This results in all the data in the database being deleted and starting fresh.
:::


## How to develop

### Changing dependencies

It's critical to update the lockfile every time dependencies are changed. Whenever you
update the `environment.yml`, please update the lockfile with:

```
conda-lock
```


### Typechecking and tests

Run all tests, including typechecking with mypy, with:

```
inv test
```


### Formatting and linting

Linting and formatting are done automatically with `pre-commit`. To configure it:

```
pre-commit install
```

After running this command, linting and formatting will occur automatically at
commit-time.

To manually trigger linting and formatting:

```
pre-commit run --all-files
```


### Third-party services

See
[our documentation on third-party services](/reference/third-party-service-dependencies.md)
for more, but the way they are currently set up should allow for development on
`localhost`.


### Coding concerns

#### Adding a new route

* Create the new route function in a module under `/routes/`
* Should the route be restricted to only logged-in users? If so, decorate with
  `@login_required`.
* If you need to create a new module and blueprint, don't forget to register the
  blueprint in `/__init__.py`


#### REST API design

* Use `resources/add` route to serve a form to add a new resource to collection
  "resources".
    * This is valuable for using HTMX to help with separation of user interface
      concerns; e.g. instead of designing a page with multiple forms, design form
      endpoints and HTMX elements on the page which use those endpoints to display the
      returned forms in a modal.
    * That form will `POST` to `resources` to actually request the resource to be
      created.
* Simple resources that only display as forms should return a form from the basic `GET`
  request to a resource endpoint, e.g. `GET resource/1`.
    * TODO: Instead of `add` as mentioned in the bullet above, perhaps we should
      standardize the form-serving endpoints as `GET resources/form`, `GET
      resource/1/form`?
* Tip: Use separate route functions for separate verbs/methods! Otherwise there can be
  excessive conditional logic inside route functions.


#### Flask route design and naming

Most importantly, **keep it simple**! Constructing route strings can be confusing
otherwise.

* Use HTTP verbs to name basic endpoint functions (`get`, `post`, `delete`, etc.).
  Resist the temptation to write descriptive route function names. Instead of
  `view_project_data_products`, stick with `get`. Then the resultant route identifier
  might be `project.data_products.get` instead of
  `project.data_products.view_project_data_products`.
    * Form-serving routes are an exception; see the "REST API design" section above.
* Use nested routes. This pushes the responsibility for route registry down the route
  hierarchy instead of requiring every blueprint to be registered in `__init__.py`.



### Debugging

#### HTMX routes

When you put a `breakpoint()` in a route that returns a partial to HTMX and try to test
in the browser, HTMX will swallow the debugger response, treating it like a failure.

You can directly visit the route in question with your browser to bypass this and access
the Flask debugger!
