"""The Value Tree Analysis assessment data model.

WARNING: The type-checker can't save you from yourself in this file; there are many
magic strings that need to match class names at runtime.

TODO: Considered documented approach at the end of this section to mitigate above
warning:
    https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#late-evaluation-of-relationship-arguments

"""
from datetime import datetime
from functools import cache
from typing import NotRequired

from flask_login import UserMixin, current_user
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey, UniqueConstraint
from sqlalchemy.types import Boolean, DateTime, Enum, Integer, String
from typing_extensions import TypedDict

from usaon_benefit_tool import db
from usaon_benefit_tool.constants.status import STATUSES

# Workaround for missing type stubs for flask-sqlalchemy:
#     https://github.com/dropbox/sqlalchemy-stubs/issues/76#issuecomment-595839159
BaseModel: DeclarativeMeta = db.Model


# TODO: This below supports linking objects to their relationships with generic names,
# but we also need to link relationships to objects with generic names (source/target).
# That's currently implemented in a WET way below.
class IORelationship(TypedDict):
    input: NotRequired[BaseModel]
    output: NotRequired[BaseModel]


# TODO: IOLinkMixin?
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
                ' input_relationships or output_relationships',
            )

        return io


# TODO: object -> node
class AssessmentObjectFieldMixin:
    """Provide shared fields between all relationship objects to reduce repetition."""

    short_name = Column(String(256), nullable=False)
    full_name = Column(String(256), nullable=True)
    organization = Column(String(256), nullable=False)
    funder = Column(String(256), nullable=False)
    funding_country = Column(String(256), nullable=False)
    # do we want another website field?
    website = Column(String(256), nullable=True)
    contact_information = Column(String(256), nullable=False)
    persistent_identifier = Column(String(256), nullable=True)
    real = Column(Boolean, nullable=False)


class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    id = Column(
        Integer,
        autoincrement=True,
        primary_key=True,
    )
    # TODO: Do we want to add google_id?
    email = Column(
        # This will be email from google sso
        String,
        nullable=False,
        unique=True,
        # we want to query by email
        index=True,
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
        default="analyst",
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

    role = relationship('Role')
    # TODO: Rename "created_assessments"? Add "filled_assessments"?
    assessments = relationship(
        'Assessment',
        back_populates='created_by',
    )


class Assessment(BaseModel):
    __tablename__ = 'assessment'
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    title = Column(
        String(128),
        nullable=False,
    )

    status_id = Column(
        String,
        ForeignKey('status.id'),
        default=STATUSES[0],
        nullable=False,
    )

    created_by_id = Column(
        Integer,
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

    description = Column(
        String(512),
        nullable=True,
    )

    private = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    created_by = relationship(
        'User',
        back_populates='assessments',
    )
    status = relationship('Status')
    nodes = relationship(
        'NodeAssessment',
        back_populates='assessment',
    )


class Node(BaseModel, IORelationshipMixin, AssessmentObjectFieldMixin):
    __tablename__ = 'node'
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    assessment_id = Column(
        Integer,
        ForeignKey('assessment.id'),
        nullable=False,
    )
    type_id = Column(
        String,
        ForeignKey('node_type.id'),
        nullable=False,
    )
    description = Column(
        String(512),
        nullable=True,
    )
    tags = Column(String, nullable=False)
    version = Column(String(64), nullable=True)
    created_by_id = Column(
        Integer,
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
    assessment = relationship(
        'Assessment',
        back_populates='nodes',
    )


class AssessmentNode(BaseModel, IORelationshipMixin, AssessmentObjectFieldMixin):
    __tablename__ = ''
    __table_args__ = (UniqueConstraint('short_name', 'assessment_id', 'node_id'),)
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    assessment_id = Column(
        Integer,
        ForeignKey('assessment.id'),
        nullable=False,
    )


# Association tables
# TODO: Rename -> AssessmentStatus?
class Status(BaseModel):
    __tablename__ = 'status'
    id = Column(
        String,
        primary_key=True,
    )
    type = Column(
        Enum(),
        nullable=False,
    )


class Role(BaseModel):
    __tablename__ = 'role'
    id = Column(
        String,
        primary_key=True,
        nullable=False,
    )


class NodeType(BaseModel):
    __tablename__ = 'role'
    id = Column(
        String,
        primary_key=True,
        nullable=False,
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
        primary_key=True,
    )

    societal_benefit_sub_area = relationship(
        'SocietalBenefitSubArea',
        back_populates='societal_benefit_key_objectives',
    )


# NOTE: not sure if we need this
AssessmentNode = (
    AssessmentObservingSystem
    | AssessmentDataProduct
    | AssessmentApplication
    | AssessmentSocietalBenefitArea
)
