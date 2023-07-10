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


