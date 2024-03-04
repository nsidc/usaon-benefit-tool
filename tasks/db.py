from invoke import task

from .util import in_container


@task(aliases=('recreate',))
def init(ctx, *, reference_data=True):
    """Drop and recreate all database tables, loading them by default.

    TODO: Enable loading test data. Currently doesn't work with error `Instance
    is not bound to a Session`. Works fine when directly running load_test_data.

    ```python
    def init(ctx, *, reference_data=True, test_data=False):
    ```
    """
    if not in_container():
        print(
            'Please run from the container context using'
            ' `scripts/invoke_in_container.sh`',
        )
        return

    from usaon_benefit_tool import create_app
    from usaon_benefit_tool.util.db.setup import recreate_tables as recreate_tables_

    app = create_app()

    # TODO: "Are you sure" confirmation?
    with app.app_context():
        print('Recreating tables...')
        recreate_tables_()

        if reference_data:
            load_reference_data(ctx)

        # if test_data:
        #     load_test_data(ctx)


@task()
def load_reference_data(ctx):
    """Populate reference tables with data."""
    if not in_container():
        print(
            'Please run from the container context using'
            ' `scripts/invoke_in_container.sh`',
        )
        return

    from usaon_benefit_tool import create_app
    from usaon_benefit_tool.util.db.setup import populate_reference_data

    app = create_app()

    with app.app_context():
        print('Loading reference tables...')
        populate_reference_data()


@task()
def load_test_data(ctx):
    """Populate operational tables with test data."""
    if not in_container():
        print(
            'Please run from the container context using'
            ' `scripts/invoke_in_container.sh`',
        )
        return

    from usaon_benefit_tool import create_app
    from usaon_benefit_tool.util.db.setup import populate_test_data

    app = create_app()

    with app.app_context():
        print('Loading test data...')
        populate_test_data()
