### Typechecking and tests

Run all tests, including typechecking with mypy, with:

```
inv test
```


### Changing dependencies

It's critical to update the lockfile every time dependencies are changed. Whenever you
update the `environment.yml`, please update the lockfile with:

```
conda-lock
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
