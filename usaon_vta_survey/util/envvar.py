import os


def envvar_is_true(envvar_name: str) -> bool:
    return os.environ.get(envvar_name, "false").lower() == "true"
