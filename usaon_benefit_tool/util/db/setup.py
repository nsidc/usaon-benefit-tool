"""Set up an existing database with the tables and/or data this application needs.

TODO: Break this up in to multiple modules!
"""
from flask import current_app
from loguru import logger
from sqlalchemy import MetaData
from sqlalchemy.orm import Session

from usaon_benefit_tool import db
from usaon_benefit_tool._types import ObservingSystemType
from usaon_benefit_tool.constants.rbac import ROLES
from usaon_benefit_tool.constants.sba import IAOA_SBA_FRAMEWORK
from usaon_benefit_tool.constants.status import STATUSES
from usaon_benefit_tool.models.tables import (
    Assessment,
    AssessmentApplication,
    AssessmentApplicationSocietalBenefitArea,
    AssessmentDataProduct,
    AssessmentDataProductApplication,
    AssessmentObservingSystem,
    AssessmentObservingSystemDataProduct,
    AssessmentSocietalBenefitArea,
    Role,
    SocietalBenefitArea,
    SocietalBenefitKeyObjective,
    SocietalBenefitSubArea,
    Status,
)
from usaon_benefit_tool.util.dev import DEV_USER


def recreate_tables() -> None:
    # Drop all tables
    reflected_md = MetaData()
    reflected_md.reflect(
        bind=db.session.get_bind(),
        views=True,
        only=lambda tablename, _: not tablename.startswith('pg_'),
    )
    reflected_md.drop_all(bind=db.session.get_bind())

    create_tables(db.session)

    db.session.commit()


def create_tables(session: Session) -> None:
    """Create all tables."""
    db.Model.metadata.create_all(bind=session.get_bind())
    logger.info('Tables created.')


def populate_reference_data() -> None:
    """Load the reference tables with data.

    Reference tables are tables containing (mostly) static data, e.g. the statuses
    table. Usually these are not editable within the GUI.
    """
    _init_societal_benefit_areas(db.session)
    _init_roles(db.session)
    _init_statuses(db.session)

    # TODO: Should this be part of test data? If so, we need to find a way to allow this
    # to only run the first time / tolerate duplicate errors.
    if current_app.config["LOGIN_DISABLED"]:
        _init_dev_user(db.session)

    logger.info('Reference data loaded.')


def populate_test_data() -> None:
    """Load the operational tables with example data."""
    _init_test_assessment(db.session)

    logger.info('Test data loaded.')


def _init_statuses(session: Session) -> None:
    session.add_all(
        [
            Status(
                id=status,
            )
            for status in STATUSES
        ],
    )

    session.commit()


def _init_roles(session: Session) -> None:
    session.add_all(
        [
            Role(
                id=role,
            )
            for role in ROLES
        ],
    )

    session.commit()


def _init_societal_benefit_areas(session: Session) -> None:
    """Insert Societal Benefit Areas from GEOSS framework.

    https://en.wikipedia.org/wiki/Global_Earth_Observation_System_of_Systems
    """
    # Add all areas:
    session.add_all(
        [
            SocietalBenefitArea(
                id=sba_name,
            )
            for sba_name in IAOA_SBA_FRAMEWORK.keys()
        ],
    )

    # Flush guarantees that these records will be present in the transaction before we
    # add the subsequent child records.
    session.flush()

    for sba_name, sba in IAOA_SBA_FRAMEWORK.items():
        # Add all of `sba`'s sub-areas:
        session.add_all(
            [
                SocietalBenefitSubArea(
                    id=sub_area_name,
                    societal_benefit_area_id=sba_name,
                )
                for sub_area_name in sba.keys()
            ],
        )
        session.flush()

        for sub_area_name, sub_area in sba.items():
            # Add all of `sub_area`'s key objectives:
            session.add_all(
                [
                    SocietalBenefitKeyObjective(
                        id=key_objective_name,
                        societal_benefit_subarea_id=sub_area_name,
                    )
                    for key_objective_name in sub_area
                ],
            )

    session.commit()


def _init_test_assessment(session: Session) -> None:
    assessment = Assessment(
        title="[TEST] This is testing data!",
        description=(
            "Created by running the relevant invoke task from the project source code."
        ),
    )

    common_obj_fields = {
        "organization": "-",
        "funder": "-",
        "funding_country": "-",
        "website": "-",
        "description": "-",
        "contact_name": "-",
        "contact_title": "-",
        "contact_email": "-",
        "tags": "-",
        "version": "-",
    }

    observing_system = AssessmentObservingSystem(
        **common_obj_fields,
        short_name="Test observing system",
        full_name="This is a test object",
        type=ObservingSystemType.other,
        assessment=assessment,
    )

    data_product = AssessmentDataProduct(
        **common_obj_fields,
        short_name="Test data product",
        full_name="This is a test object",
        assessment=assessment,
    )
    observing_system_data_product = AssessmentObservingSystemDataProduct(
        performance_rating=50,
        criticality_rating=10,
        observing_system=observing_system,
        data_product=data_product,
    )

    application = AssessmentApplication(
        **common_obj_fields,
        short_name="Test application",
        full_name="This is a test object",
        performance_criteria="",
        performance_rating=90,
        assessment=assessment,
    )
    data_product_application = AssessmentDataProductApplication(
        performance_rating=75,
        criticality_rating=20,
        data_product=data_product,
        application=application,
    )

    sba = AssessmentSocietalBenefitArea(
        societal_benefit_area_id=next(iter(IAOA_SBA_FRAMEWORK.keys())),
        assessment=assessment,
    )
    application_sba = AssessmentApplicationSocietalBenefitArea(
        performance_rating=25,
        application=application,
        societal_benefit_area=sba,
    )

    session.add_all(
        [
            assessment,
            observing_system,
            data_product,
            observing_system_data_product,
            application,
            data_product_application,
            sba,
            application_sba,
        ],
    )
    session.commit()


def _init_dev_user(session: Session) -> None:
    logger.warning("Inserting dev user. This should not happen in production!")
    session.add(DEV_USER)
    session.commit()
