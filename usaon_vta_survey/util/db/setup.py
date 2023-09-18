from loguru import logger
from sqlalchemy import MetaData
from sqlalchemy.orm import Session

from usaon_vta_survey import create_app, db
from usaon_vta_survey.constants.roles import ROLES
from usaon_vta_survey.constants.sba import IAOA_SBA_FRAMEWORK
from usaon_vta_survey.constants.status import STATUSES
from usaon_vta_survey.models.tables import (
    Role,
    SocietalBenefitArea,
    SocietalBenefitKeyObjective,
    SocietalBenefitSubArea,
    Status,
)
from usaon_vta_survey.util.dev import DEV_USER

app = create_app()


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
    # Create all tables
    db.Model.metadata.create_all(bind=session.get_bind())
    logger.info('Tables created.')


def populate_reference_data() -> None:
    init_societal_benefit_areas(db.session)
    init_roles(db.session)
    init_statuses(db.session)

    if app.config["LOGIN_DISABLED"]:
        init_dev_user(db.session)

    logger.info('Reference data loaded.')


def init_statuses(session: Session) -> None:
    session.add_all(
        [
            Status(
                id=status,
            )
            for status in STATUSES
        ]
    )

    session.commit()


def init_roles(session: Session) -> None:
    session.add_all(
        [
            Role(
                id=role,
            )
            for role in ROLES
        ]
    )

    session.commit()


def init_dev_user(session: Session) -> None:
    logger.warning("Inserting dev user. This should not happen in production!")
    session.add(DEV_USER)
    session.commit()


def init_societal_benefit_areas(session: Session) -> None:
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
        ]
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
            ]
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
                ]
            )

    session.commit()
