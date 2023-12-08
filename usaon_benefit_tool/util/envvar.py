import os


def envvar_is_true(envvar_name: str) -> bool:
    """Return `True` if environment variable is set with the value 'true'.

    Case insensitive.
    """
    return os.environ.get(envvar_name, "false").lower() == "true"
