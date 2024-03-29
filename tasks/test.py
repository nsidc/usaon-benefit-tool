import sys
from pathlib import Path

from invoke import task

from .util import print_and_run

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(PROJECT_DIR)

# WARNING: Do not import from usaon_benefit_tool at this level to avoid failure of basic
# commands because unneeded envvars are not populated.


@task(aliases=['mypy'])
def typecheck(ctx):
    """Run mypy static type analysis."""
    from usaon_benefit_tool.constants.paths import PACKAGE_DIR

    print_and_run(f'cd {PROJECT_DIR} && mypy {PACKAGE_DIR}')
    print('🎉🦆 Type checking passed.')


@task(
    pre=[typecheck],
    default=True,
)
def default(ctx):
    """Run all tasks."""
    print('🎉❤️  All tests passed!')
