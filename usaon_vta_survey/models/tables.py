"""The VTA survey data model.

WARNING: The type-checker can't save you from yourself in this file; there are many
magic strings that need to match class names at runtime.

TODO: Considered documented approach at the end of this section to mitigate above
warning:
    https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#late-evaluation-of-relationship-arguments

TODO: Add check constraints for numeric fields where we know the min/max.
"""
import uuid
from datetime import datetime
from functools import cache
from typing import Final

from flask_login import UserMixin, current_user
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.types import DateTime, Enum, Integer, SmallInteger, String
from typing_extensions import NotRequired, TypedDict

from usaon_vta_survey import db
from usaon_vta_survey._types import ObservingSystemType

# Workaround for missing type stubs for flask-sqlalchemy:
#     https://github.com/dropbox/sqlalchemy-stubs/issues/76#issuecomment-595839159
BaseModel: DeclarativeMeta = db.Model


class IORelationship(TypedDict):
    input: NotRequired[BaseModel]
    output: NotRequired[BaseModel]


class IORelationshipMixin:
    """Provide a dictionary of input and/or output models related to this entity.

    TODO: Could use a clearer name. We may want to also have a mixin for models
    representing relationships instead of entities.
    """

    @classmethod
    @cache
    def __io__(cls) -> IORelationship:
        """Return dictionary of any IO relationships this model has.

        TODO: Fix and remove type-ignore comments.
        """
        io: IORelationship = {}
        if hasattr(cls, 'input_relationships'):
            io['input'] = cls.input_relationships.mapper.class_  # type: ignore
        if hasattr(cls, 'output_relationships'):
            io['output'] = cls.output_relationships.mapper.class_  # type: ignore

        if io == {}:
            raise RuntimeError(
                'Please only use IORelationshipMixin on a model with'
                ' input_relationships or output_relationships'
            )

        return io


class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    id = Column(
        # This will be email from google sso
        String,
        primary_key=True,
        nullable=False,
    )
    name = Column(
        String,
        nullable=False,
    )
    orcid = Column(
        String(64),  # how long are orcids?
        nullable=True,
    )
    role_id = Column(
        String,
        ForeignKey('role.id'),
        default="admin",
        nullable=False,
    )
    biography = Column(
        String,
        nullable=True,
    )
    affiliation = Column(
        String,
        nullable=True,
    )


class Survey(BaseModel):
    __tablename__ = 'survey'
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    response_id = Column(
        Integer,
        ForeignKey('response.id'),
        nullable=True,
    )

    title = Column(
        String(128),
        nullable=False,
    )

    created_by = Column(
        String,
        ForeignKey('user.id'),
        default=(lambda: current_user.id),
        nullable=False,
    )

    created_timestamp = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
    )
    notes = Column(
        String(512),
        nullable=True,
    )

    response = relationship(
        'Response',
        back_populates='survey',
    )


class Response(BaseModel):
    __tablename__ = 'response'
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    created_by = Column(
        String,
        ForeignKey('user.id'),
        default=(lambda: current_user.id),
        nullable=False,
    )
    created_timestamp = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
    )
    updated_timestamp = Column(
        DateTime,
        nullable=False,
        default=datetime.now,
    )

    survey = relationship(
        'Survey',
        back_populates='response',
    )
    observing_systems = relationship(
        'ResponseObservingSystem',
        back_populates='response',
    )
    data_products = relationship(
        'ResponseDataProduct',
        back_populates='response',
    )
    applications = relationship(
        'ResponseApplication',
        back_populates='response',
    )
    societal_benefit_areas = relationship(
        'ResponseSocietalBenefitArea',
        back_populates='response',
    )


class ResponseObservingSystem(BaseModel, IORelationshipMixin):
    __tablename__ = 'response_observing_system'
    __table_args__ = (UniqueConstraint('name', 'response_id'),)
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name = Column(
        String(256),
        nullable=False,
    )
    response_id = Column(
        Integer,
        ForeignKey('response.id'),
        nullable=False,
    )

    type = Column(
        Enum(ObservingSystemType),
        nullable=False,
    )

    __mapper_args__: Final[dict] = {
        'polymorphic_identity': ObservingSystemType.other,
        'polymorphic_on': type,
    }

    url = Column(String(256), nullable=False)
    author_name = Column(String(256), nullable=False)
    author_email = Column(String(256), nullable=False)
    funding_country = Column(String(256), nullable=False)
    funding_agency = Column(String(256), nullable=False)
    references_citations = Column(String(512), nullable=False)
    notes = Column(String(512), nullable=True)

    response = relationship(
        'Response',
        back_populates='observing_systems',
    )
    output_relationships = relationship(
        'ResponseObservingSystemDataProduct',
        back_populates='observing_system',
    )


class ResponseObservingSystemObservational(BaseModel):
    __tablename__ = 'response_observing_system_observational'
    __mapper_args__: Final[dict] = {
        'polymorphic_identity': ObservingSystemType.observational,
    }

    response_observing_system_id = Column(
        Integer,
        ForeignKey('response_observing_system.id'),
        primary_key=True,
    )

    platform = Column(String(256), nullable=False)
    sensor = Column(String(256), nullable=False)


class ResponseObservingSystemResearch(BaseModel):
    __tablename__ = 'response_observing_system_research'
    __mapper_args__: Final[dict] = {
        'polymorphic_identity': ObservingSystemType.research,
    }

    response_observing_system_id = Column(
        Integer,
        ForeignKey('response_observing_system.id'),
        primary_key=True,
    )

    intermediate_product = Column(String(256), nullable=False)


class ResponseDataProduct(BaseModel, IORelationshipMixin):
    __tablename__ = 'response_data_product'
    __table_args__ = (UniqueConstraint('name', 'response_id'),)
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name = Column(
        String(256),
        nullable=False,
    )
    response_id = Column(
        Integer,
        ForeignKey('response.id'),
        nullable=False,
    )

    # TODO: Constrain to 0-100
    performance_rating = Column(
        SmallInteger,
        nullable=False,
    )

    response = relationship(
        'Response',
        back_populates='data_products',
    )
    input_relationships = relationship(
        'ResponseObservingSystemDataProduct',
        back_populates='data_product',
    )
    output_relationships = relationship(
        'ResponseDataProductApplication',
        back_populates='data_product',
    )


class ResponseApplication(BaseModel, IORelationshipMixin):
    __tablename__ = 'response_application'
    __table_args__ = (UniqueConstraint('name', 'response_id'),)
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name = Column(
        String(256),
        nullable=False,
    )
    response_id = Column(
        Integer,
        ForeignKey('response.id'),
        nullable=False,
    )

    response = relationship(
        'Response',
        back_populates='applications',
    )
    input_relationships = relationship(
        'ResponseDataProductApplication',
        back_populates='application',
    )
    output_relationships = relationship(
        'ResponseApplicationSocietalBenefitArea',
        back_populates='application',
    )


class ResponseSocietalBenefitArea(BaseModel, IORelationshipMixin):
    __tablename__ = 'response_societal_benefit_area'
    __table_args__ = (UniqueConstraint('societal_benefit_area_id', 'response_id'),)
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    response_id = Column(
        Integer,
        ForeignKey('response.id'),
        nullable=False,
    )

    societal_benefit_area_id = Column(
        String(256),
        ForeignKey('societal_benefit_area.id'),
        nullable=False,
    )

    response = relationship(
        'Response',
        back_populates='societal_benefit_areas',
    )
    societal_benefit_area = relationship('SocietalBenefitArea')
    input_relationships = relationship(
        'ResponseApplicationSocietalBenefitArea',
        back_populates='societal_benefit_area',
    )


# Association tables
class Role(BaseModel):
    __tablename__ = 'role'
    id = Column(
        String,
        primary_key=True,
        nullable=False,
    )


class ResponseObservingSystemDataProduct(BaseModel):
    __tablename__ = 'response_observing_system_data_product'
    response_observing_system_id = Column(
        Integer,
        ForeignKey('response_observing_system.id'),
        primary_key=True,
    )
    response_data_product_id = Column(
        Integer,
        ForeignKey('response_data_product.id'),
        primary_key=True,
    )

    # TODO: Constrain ratings 0-100
    criticality_rating = Column(SmallInteger, nullable=False)
    performance_rating = Column(SmallInteger, nullable=False)
    rationale = Column(String(512), nullable=True)
    needed_improvements = Column(String(512), nullable=True)

    observing_system = relationship(
        'ResponseObservingSystem',
        back_populates='output_relationships',
    )
    data_product = relationship(
        'ResponseDataProduct',
        back_populates='input_relationships',
    )


class ResponseDataProductApplication(BaseModel):
    __tablename__ = 'response_data_product_application'
    response_data_product_id = Column(
        Integer,
        ForeignKey('response_data_product.id'),
        primary_key=True,
    )
    response_application_id = Column(
        Integer,
        ForeignKey('response_application.id'),
        primary_key=True,
    )

    # TODO: Constrain ratings 0-100
    criticality_rating = Column(SmallInteger, nullable=False)
    performance_rating = Column(SmallInteger, nullable=False)
    rationale = Column(String(512), nullable=True)
    needed_improvements = Column(String(512), nullable=True)

    data_product = relationship(
        'ResponseDataProduct',
        back_populates='output_relationships',
    )
    application = relationship(
        'ResponseApplication',
        back_populates='input_relationships',
    )


class ResponseApplicationSocietalBenefitArea(BaseModel):
    __tablename__ = 'response_application_societal_benefit_area'
    response_application_id = Column(
        Integer,
        ForeignKey('response_application.id'),
        primary_key=True,
    )
    response_societal_benefit_area_id = Column(
        Integer,
        ForeignKey('response_societal_benefit_area.id'),
        primary_key=True,
    )

    # TODO: Constrain ratings 0-100
    performance_rating = Column(SmallInteger, nullable=False)

    application = relationship(
        'ResponseApplication',
        back_populates='output_relationships',
    )
    societal_benefit_area = relationship(
        'ResponseSocietalBenefitArea',
        back_populates='input_relationships',
    )


# Reference tables
class SocietalBenefitArea(BaseModel):
    __tablename__ = 'societal_benefit_area'
    id = Column(
        String(256),
        primary_key=True,
    )

    societal_benefit_sub_areas = relationship(
        'SocietalBenefitSubArea',
        back_populates='societal_benefit_area',
    )


class SocietalBenefitSubArea(BaseModel):
    __tablename__ = 'societal_benefit_subarea'
    id = Column(
        String(256),
        primary_key=True,
    )
    societal_benefit_area_id = Column(
        String(256),
        ForeignKey('societal_benefit_area.id'),
        nullable=False,
    )

    societal_benefit_area = relationship(
        'SocietalBenefitArea',
        back_populates='societal_benefit_sub_areas',
    )
    societal_benefit_key_objectives = relationship(
        'SocietalBenefitKeyObjective',
        back_populates='societal_benefit_sub_area',
    )


class SocietalBenefitKeyObjective(BaseModel):
    __tablename__ = 'societal_benefit_key_objective'
    id = Column(
        String(256),
        primary_key=True,
    )
    societal_benefit_subarea_id = Column(
        String(256),
        ForeignKey('societal_benefit_subarea.id'),
        nullable=False,
    )

    societal_benefit_sub_area = relationship(
        'SocietalBenefitSubArea',
        back_populates='societal_benefit_key_objectives',
    )
