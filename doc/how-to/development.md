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

# Mark Alembic as up-to-date 
# this creates the alembic table on the dev DB and puts in the most recent migration ID
# essential for doing future migrations
docker compose run --rm usaon-benefit-tool alembic stamp head
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

**The stack should now be up, with the web interface running at `localhost:5000`, and
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


### Database migrations

Database migrations are managed by [Alembic](https://alembic.sqlalchemy.org/).

Configuration exists in the `migrations/` directory. Migrations themselves live in
`migrations/versions/` directories. They are named with unique identifiers, and they are
**not in chronological order**. The migration script itself contains information about
its dependencies. Each migration depends on the one before it.

**When the data model changes, you must
[create a database migration (a.k.a. "revision")](https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script).
Each release should contain either 0 or 1 database migrations.** If you make multiple
changes within a single release cycle, combine them all into one migration.

Create each revision with a descriptive name, following the convention you would use
when creating a Git commit.

:::{.callout-important}
These commands are executed within the Docker stack by prefixing `docker compose run
--rm usaon-benefit-tool` to the `alembic` command. The database must be running.
:::

```bash
docker compose run --rm usaon-benefit-tool alembic revision --autogenerate --message "Add new criticality rationale field"
```

This will scan the database and data model for changes and produce an automated
migration, creating a new file in `migrations/versions/` directory. **Review and test
this migration carefully.** Remember, the data in the database needs to be changed, not
just the columns.

To generate an empty migration and manually populate the behaviors, omit
`--autogenerate`.

To apply all migrations and bring the DB to the latest state:

```bash
docker compose run --rm usaon-benefit-tool alembic upgrade head  # or replace "head" with a migration id
```

Finally, create an executable post-deploy script matching the release which should
include the new migration in `deploy/post/` directory, e.g. `deploy/post/v2.1.0`.


### Third-party services

See
[our documentation on third-party services](/reference/third-party-service-dependencies.md)
for more, but the way they are currently set up should allow for development on
`localhost`.


### Coding concerns

#### Adding a new route

> [!IMPORTANT]
>
> Implement access control at the route level, instead of the template. You may still
> need some role-based conditionals in templates to, for example, hide a button. Avoid
> leaving holes where end-users can still use a tool like cURL to submit an update
> request without authentication or authorization.

* Create the new route function in a module under `/routes/`
* Should the route be restricted to only logged-in users? If so, decorate with
  `@login_required`.
* If you need to create a new module and blueprint, don't forget to register the
  blueprint in `/__init__.py`


#### REST API design

* Use `.../form` endpoints for HTMX to get user interface elements.
    * This is valuable for using HTMX to help with separation of user interface
      concerns; e.g. instead of designing a page with multiple forms, design form
      endpoints and HTMX elements on the page which use those endpoints to display the
      returned forms in a modal.
    * Use `GET resources/form` route to serve a form to add a new resource to collection
      "resources".
        * That form will `POST resources` to request the resource to be created.
    * Use `GET resource/<id>/form` route to serve a form to edit a "resource".
        * That form will `PUT resource/<id>` to request the resource to be updated.
* Use consistent HTTP response codes:
    * `200`: Successfully returned page or successfully updated resource
    * `201`: Create resource
    * `202`: Successfully deleted resource
    * ...
* Avoid redirections after operations, e.g. after a delete, don't `302`. Instead,
  `202` and pass an `HX-Redirect` header to inform HTMX, if used on the client side,
  what to do.
* Use separate route functions for separate verbs/methods! Otherwise there can be
  excessive conditional logic inside route functions.


#### Flask route design and naming

Most importantly, **keep it simple**! Constructing route strings can be confusing
otherwise.

* Use HTTP verbs to name basic endpoint functions (`get`, `post`, `delete`, etc.).
  Resist the honorable temptation to write descriptive route function names. Instead of
  `view_project_data_products`, stick with `get`. Then the resultant route identifier
  might be `project.data_products.get` instead of
  `project.data_products.view_project_data_products`.
    * Form-serving routes are an exception; see the "REST API design" section above.
* Use nested routes. This pushes the responsibility for route registry down the route
  hierarchy instead of requiring every blueprint to be registered in `__init__.py`.


#### Flask template design and naming

##### Macros

* Macros live in `templates/macros/`
* Macros that output HTML should be prefixed with `render_`. The codebase is currently
  not in compliance with this.


### Debugging

#### HTMX routes

When you put a `breakpoint()` in a route that returns a partial to HTMX and try to test
in the browser, HTMX will swallow the debugger response, treating it like a failure.

You can directly visit the route in question with your browser to bypass this and access
the Flask debugger! However, the HTMX Javascript won't load, so you can't really use
this to debug forms.
