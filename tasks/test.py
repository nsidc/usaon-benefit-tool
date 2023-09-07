import os
import sys
from pathlib import Path

from invoke import task

from .util import print_and_run

# NOTE: This is a hack, we want to be able to run pytest
# without setting environment variables.
os.environ['USAON_VTA_DB_SQLITE'] = 'true'
os.environ['FLASK_DEBUG'] = 'true'
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(PROJECT_DIR)

# WARNING: Do not import from usaon_vta_survey at this level to avoid failure of basic
# commands because unneeded envvars are not populated.


@task(aliases=['mypy'])
def typecheck(ctx):
    """Run mypy static type analysis."""
    from usaon_vta_survey.constants.paths import PACKAGE_DIR

    print_and_run(
        f'cd {PROJECT_DIR} &&'
        f' mypy --config-file={PROJECT_DIR}/.mypy.ini {PACKAGE_DIR}',
    )
    print('🎉🦆 Type checking passed.')


@task()
def unit(ctx):
    """Run unit tests."""
    print_and_run(f'cd {PROJECT_DIR} && pytest')
    print('🎉🦆 Unit checking passed.')


@task(
    pre=[typecheck],
    default=True,
)
def default(ctx):
    """Run all tasks."""
    print('🎉❤️  All tests passed!')
