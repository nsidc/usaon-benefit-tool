FROM mambaorg/micromamba:1.5.0

# TODO: Figure out a better way to run tasks without requiring container
# configuration
RUN touch "/tmp/i_am_the_usaon-benefit-tool_container"

WORKDIR /usaon-benefit-tool

# Activate the conda environment during build process
ARG MAMBA_DOCKERFILE_ACTIVATE=1

COPY ./conda-lock.yml .

RUN micromamba install -y \
    # NOTE: -p is important to install to the "base" env
    -p /opt/conda \
    -f conda-lock.yml
RUN micromamba clean --all --yes


# Install source
COPY ./setup.py .
COPY ./pyproject.toml .
COPY ./.mypy.ini .
COPY ./tasks ./tasks
COPY ./usaon_benefit_tool ./usaon_benefit_tool

ENV FLASK_APP=usaon_benefit_tool


# Test dependencies
RUN python -c "import flask"
RUN which flask

# Start a flask server
#
# WARNING: Be careful not to change this CMD to an ENTRYPOINT without reading
# the docs!
#     https://micromamba-docker.readthedocs.io/en/latest/advanced_usage.html#use-of-the-entrypoint-command-within-a-dockerfile
#
# For gunicorn, the recommended number of workers is (2*CPU)+1. This config
# assumes dual-core CPU.
CMD ["gunicorn", "usaon_benefit_tool:app", "--workers", "5", "--bind", "0.0.0.0:5000"]
