# Development

## How to run the application for development

### Deploy the development database

Deploy [usaon-vta-db](https://github.com/nsidc/usaon-vta-db) and follow instructions in
that repo.


### Symlink dev config

```bash
ln -s docker-compose.dev.yml docker-compose.override.yml
```


### Define environment variables

Define the environment variables as specified in [envvars.md](./envvars.md):

```bash
export DB_HOST=...
export DB_PORT=...
export DB_USER=...
export DB_PASSWORD=...
```

### Start the service

Bring up the docker container:

```bash
docker-compose up -d
```


### Initialize the database

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
