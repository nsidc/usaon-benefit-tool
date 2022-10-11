from pathlib import Path

from invoke import task

from .util import in_container


@task(aliases=('recreate',))
def init(ctx, load=True):
    """Drop and recreate all database tables, loading them by default."""
    if not in_container():
        print('Please run from the container context')

    from usaon_vta_survey.util.db.setup import recreate_tables as recreate_tables_

    # TODO: "Are you sure" confirmation?
    print('Recreating tables...')
    recreate_tables_()

    if load:
        print('Loading reference tables...')
        load_reference_data(ctx)


@task()
def load_reference_data(ctx):
    """Populate reference tables with data."""
    if not in_container():
        print('Please run from the container context')

    from usaon_vta_survey.util.db.setup import populate_reference_data

    populate_reference_data()
