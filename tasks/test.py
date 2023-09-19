import sys
from pathlib import Path

from invoke import task

from .util import print_and_run

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(PROJECT_DIR)

# WARNING: Do not import from usaon_vta_survey at this level to avoid failure of basic
# commands because unneeded envvars are not populated.


@task(aliases=['mypy'])
def typecheck(ctx):
    """Run mypy static type analysis."""
    from usaon_vta_survey.constants.paths import PACKAGE_DIR

    # os.environ['USAON_VTA_DB_SQLITE'] = 'true'
    # os.environ['FLASK_DEBUG'] = 'true'
    print_and_run(
        f'cd {PROJECT_DIR} &&'
        f' mypy --config-file={PROJECT_DIR}/.mypy.ini {PACKAGE_DIR}',
        # env={'USAON_VTA_DB_SQLITE': 'true', 'FLASK_DEBUG': 'true'},
    )
    print('🎉🦆 Type checking passed.')


@task(
    pre=[typecheck],
    default=True,
)
def default(ctx):
    """Run all tasks."""
    print('🎉❤️  All tests passed!')
