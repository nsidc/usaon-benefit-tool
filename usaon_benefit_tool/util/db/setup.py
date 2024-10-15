"""Set up an existing database with the tables and/or data this application needs.

Todo:
----
* Break this up in to multiple modules!
* Execute each function within a transaction.

"""

import sqlalchemy
from flask import current_app
from loguru import logger
from sqlalchemy import MetaData
from sqlalchemy.orm import Session

from usaon_benefit_tool import db
from usaon_benefit_tool._types import NodeType, RoleName
from usaon_benefit_tool.constants.status import ASSESSMENT_STATUSES
from usaon_benefit_tool.models.tables import (
    Assessment,
    AssessmentNode,
    AssessmentNodeSubtypeApplication,
    AssessmentStatus,
    Link,
    NodeSubtypeOther,
    NodeSubtypeSocietalBenefitArea,
    Role,
    User,
)
from usaon_benefit_tool.util.dev import DEV_USER, TEST_USER


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
    logger.success('Tables created.')


def populate_reference_data() -> None:
    """Load the reference tables with data.

    Reference tables are tables containing (mostly) static data, e.g. the statuses
    table. Usually these are not editable within the GUI.
    """
    _init_roles(db.session)
    _init_statuses(db.session)

    # TODO: Should this be part of test data? If so, we need to find a way to allow this
    # to only run the first time / tolerate duplicate errors.
    if current_app.config["LOGIN_DISABLED"]:
        _init_dev_user(db.session)

    logger.success('Reference data loaded.')


def populate_test_data() -> None:
    """Load the operational tables with example data."""
    _init_test_assessment(db.session)

    logger.success('Test data loaded.')


def _init_statuses(session: Session) -> None:
    session.add_all(
        [
            AssessmentStatus(
                id=status,
                description=description,
            )
            for status, description in ASSESSMENT_STATUSES.items()
        ],
    )

    session.commit()


def _init_roles(session: Session) -> None:
    session.add_all([Role(id=role) for role in RoleName])

    session.commit()


def _init_test_assessment(session: Session) -> None:
    test_user = _get_or_create_test_user(session)

    assessment = Assessment(
        title="[TEST] This is testing data!",
        description=(
            "Created by running the relevant invoke task from the project source code."
        ),
        created_by=test_user,
    )

    common_obj_fields = {
        "created_by": test_user,
        "organization": "-",
        "funder": "-",
        "funding_country": "-",
        "website": "-",
        "description": "This was inserted by an automated script.",
        "contact_information": "-",
        "hypothetical": False,
        # "contact_name": "-",
        # "contact_title": "-",
        # "contact_email": "-",
        # "tags": "-",
        # "version": "-",
    }

    observing_system = NodeSubtypeOther(
        **common_obj_fields,
        title="This is a test observing system",
        short_name="Test observing system",
        type=NodeType.OBSERVING_SYSTEM,
    )
    data_product = NodeSubtypeOther(
        **common_obj_fields,
        title="This is a test data product",
        short_name="Test data product",
        type=NodeType.DATA_PRODUCT,
    )
    application = NodeSubtypeOther(
        **common_obj_fields,
        title="This is a test application",
        short_name="Test application",
        type=NodeType.APPLICATION,
    )
    sba = NodeSubtypeSocietalBenefitArea(
        title="This is a test SBA",
        short_name="Test SBA",
        type=NodeType.SOCIETAL_BENEFIT_AREA,
        created_by=test_user,
    )

    assessment_observing_system = AssessmentNode(
        assessment=assessment,
        node=observing_system,
    )
    assessment_data_product = AssessmentNode(
        assessment=assessment,
        node=data_product,
    )
    os_dp_link = Link(
        source_assessment_node=assessment_observing_system,
        target_assessment_node=assessment_data_product,
        performance_rating=25,
        criticality_rating=7,
    )

    assessment_application = AssessmentNodeSubtypeApplication(
        assessment=assessment,
        node=application,
        performance_rating=15,
        performance_rating_criteria="Whatever",
        performance_rating_rationale="Dunno",
        performance_rating_gaps="C'mon that's enough questions",
    )
    dp_app_link = Link(
        source_assessment_node=assessment_data_product,
        target_assessment_node=assessment_application,
        performance_rating=50,
        criticality_rating=5,
    )

    assessment_sba = AssessmentNode(
        assessment=assessment,
        node=sba,
    )
    app_sba_link = Link(
        source_assessment_node=assessment_application,
        target_assessment_node=assessment_sba,
        performance_rating=75,
        criticality_rating=2,
    )

    session.add_all(
        [
            assessment,
            observing_system,
            data_product,
            application,
            sba,
            assessment_observing_system,
            assessment_data_product,
            assessment_application,
            assessment_sba,
            os_dp_link,
            dp_app_link,
            app_sba_link,
        ],
    )
    session.commit()


def _init_dev_user(session: Session) -> None:
    logger.warning("Inserting dev user. This should not happen in production!")
    session.add(DEV_USER)
    session.commit()


def _get_or_create_test_user(session: Session) -> User:
    """Insert a test user if it doesn't already exist."""
    try:
        # Look up test user by email address with .one()
        return User.query.filter_by(email=TEST_USER.email).one()
    except sqlalchemy.orm.exc.NoResultFound:
        logger.warning("Inserting test user.")
        session.add(TEST_USER)
        session.commit()
        return TEST_USER
