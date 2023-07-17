FROM mambaorg/micromamba:0.23.3

# TODO: Figure out a better way to run tasks without requiring container
# configuration
RUN touch "/tmp/i_am_the_usaon-vta-survey_container"

WORKDIR /usaon-vta-survey

# Activate the conda environment during build process
ARG MAMBA_DOCKERFILE_ACTIVATE=1

COPY ./conda-lock.yml .

RUN micromamba create -n usaon-vta-survey -f conda-lock.yml

# RUN micromamba clean --all --yes
RUN micromamba install -y \
    # NOTE: -p is important to install to the "base" env
    -p /opt/conda \
    -f conda-lock.yml

# Seemed like conda-lock was a bit off about the pip installs
RUN pip install wtforms_sqlalchemy
RUN pip install flask-dance

# Install source
COPY ./setup.py .
COPY ./pyproject.toml .
COPY ./.mypy.ini .
COPY ./tasks ./tasks
COPY ./usaon_vta_survey ./usaon_vta_survey

ENV FLASK_APP=usaon_vta_survey


# Did the build work?
RUN python -c "import flask"
RUN which flask

# TODO: Move this to dev docker-compose and use a production ready server option
# Start a flask server
# WARNING: Using CMD is key; using ENTRYPOINT overrides the micromamba
# entrypoint and prevents env activation.
CMD ["flask", "run", "-h", "0.0.0.0"]
