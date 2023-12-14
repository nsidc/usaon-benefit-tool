# Development

## How to run the application for development


### Symlink dev config

```bash
ln -s docker-compose.dev.yml docker-compose.override.yml
```


### Define environment variables

Define the environment variables as specified in [envvars.md](/reference/envvars.md):

```bash
export USAON_BENEFIT_TOOL_DB_HOST=...
export USAON_BENEFIT_TOOL_DB_PORT=...
export USAON_BENEFIT_TOOL_DB_USER=...
export USAON_BENEFIT_TOOL_DB_PASSWORD=...
```

> :memo: these can be put in a `.env` file so that all variables are assigned. This file
> is part of `.gitignore` so that no secrets are committed to github. 

### Start the service

Bring up the docker container:

```bash
docker compose up -d
```


### Initialize the database

> :memo: In dev this will initialize the SQLite DB. In all other environments we deploy
> the db using the [usaon-vta-db project](https://github.com/nsidc/usaon-vta-db).

Run `./scripts/invoke_in_container.sh db.init`

This can also be used to drop and recreate all the tables.

> :warning: This results in all the data in the database being deleted.


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


## How to release

### CHANGELOG

Author a new changelog section titled `NEXT_VERSION`. The `bumpversion` step will
replace this magic string with a correct version identification.


### Bump the version

We're currently pre-1.0, so all bumps should look like:

```bash
bumpversion minor
```

Post-1.0, it's OK to bump other version parts.


### Release

After everything is merged, create a release in the GitHub UI.

Releases that are `<1.0` or labeled `alpha`, `beta`, or `rc` must be marked as
pre-releases.

After the release is created, GitHub Actions will start building the container images.
Once GitHub Actions is done, you can deploy the app (`deploy/deploy`).

At NSIDC, this release should be done with Garrison.


## Third-party services

### Google SSO

A Google OAuth application is required for login to work. Our app requires a client ID
and client secret to communicate with the Google OAuth application.


### Initial setup

_TODO_


### Redirect URIs

> :warning: This configuration needs to be updated for every unique deployment URL of
> this app.

Our app's deployed URIs also must be registered with Google as ["Authorized redirect
URIs"](https://console.cloud.google.com/apis/credentials) (from the link, click on your
app under the "OAuth 2.0 Client IDs" section). The following URIs should be provided for
local development:

* `http://localhost:5000/google_oauth/google/authorized`
* `http://127.0.0.1:5000/google_oauth/google/authorized`

Add more URIs (substituting the protocol, hostname, and port number, and nothing else)
for each separate deployment.
