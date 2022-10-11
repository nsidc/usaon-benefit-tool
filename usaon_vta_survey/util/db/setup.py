import datetime as dt

from loguru import logger
from sqlalchemy import MetaData, delete
from sqlalchemy.orm import Session

from usaon_vta_survey import db
from usaon_vta_survey.constants.sba import IAOA_SBA_FRAMEWORK
from usaon_vta_survey.models.tables import (
    SocietalBenefitArea,
    SocietalBenefitSubArea,
    SocietalBenefitKeyObjective,
)


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

    populate_reference_data(db.session)
    db.session.commit()


def create_tables(session: Session) -> None:
    # Create all tables
    db.Model.metadata.create_all(bind=session.get_bind())
    logger.info('Tables created.')


def populate_reference_data(session: Session) -> None:
    init_societal_benefit_areas(session)

    logger.info('Reference data loaded.')


def init_societal_benefit_areas(session: Session) -> None:
    """Insert Societal Benefit Areas from GEOSS framework.

    https://en.wikipedia.org/wiki/Global_Earth_Observation_System_of_Systems
    """
    # Add all areas:
    session.add_all([
        SocietalBenefitArea(
            id=sba_name,
        ) for sba_name in IAOA_SBA_FRAMEWORK.keys()
    ])

    for sba_name, sba in IAOA_SBA_FRAMEWORK.items():
        # Add all of `sba`'s sub-areas:
        session.add_all([
            SocietalBenefitSubArea(
                id=sub_area_name,
                societal_benefit_area_id=sba_name,
            ) for sub_area_name in sba.keys()
        ])

        for sub_area_name, sub_area in sba.items():
            # Add all of `sub_area`'s key objectives:
            session.add_all([
                SocietalBenefitKeyObjective(
                    id=key_objective_name,
                    societal_benefit_sub_area_id=sub_area_name,
                ) for key_objective_name in sub_area
            ])
