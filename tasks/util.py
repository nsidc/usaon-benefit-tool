from functools import cache
from pathlib import Path

from invoke import run

PROJECT_DIR = Path(__file__).parent.parent


def print_and_run(cmd, **run_kwargs):
    # os.environ['FLASK_DEBUG'] = 'true'
    # os.environ['USAON_VTA_DB_SQLITE'] = 'true'
    print(cmd)
    kwargs = {
        'pty': True,
        **run_kwargs,
    }
    return run(cmd, **kwargs)


@cache
def in_container() -> bool:
    """Check for signs we're in a container.

    This is a hack to enforce a single docker-driven configuration for connecting to the
    database.
    """
    if Path('/tmp/i_am_the_usaon-vta-survey_container').is_file():
        return True

    return False
