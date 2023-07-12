# from invoke import task
#
# from .util import PROJECT_DIR, print_and_run
#
#
# @task(default=True)
# def format(ctx):
#     """Apply formatting standards to the codebase."""
#     # Black 22.1 has problems with string handling. We can work around those with
#     # `fmt: on` and `fmt: off` comments, but that's not fun.
#     #
#     #     https://github.com/psf/black/issues/2188
#     print_and_run(f"black {PROJECT_DIR}")
