"""The Value Tree Analysis assessment data model.

WARNING: The type-checker can't save you from yourself in this file; there are many
magic strings that need to match class names at runtime.

TODO: Considered documented approach at the end of this section to mitigate above
warning:
    https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#late-evaluation-of-relationship-arguments

"""
from datetime import datetime
from typing import Final

from flask_login import UserMixin, current_user
from sqlalchemy import CheckConstraint, case
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey, Index, UniqueConstraint
from sqlalchemy.types import Boolean, DateTime, Enum, Integer, String

from usaon_benefit_tool import db
from usaon_benefit_tool._types import NodeType, NodeTypeDiscriminator
from usaon_benefit_tool.constants.status import ASSESSMENT_STATUSES

# Workaround for missing type stubs for flask-sqlalchemy:
#     https://github.com/dropbox/sqlalchemy-stubs/issues/76#issuecomment-595839159
BaseModel: DeclarativeMeta = db.Model


####################
# Association tables
####################


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
        String(64),  # TODO: Exactly how long are orcids? Validator?
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
    nodes = relationship(
        'Node',
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

    description = Column(
        String(512),
        nullable=True,
    )

    private = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    status_id = Column(
        String,
        ForeignKey('status.id'),
        default=next(iter(ASSESSMENT_STATUSES.keys())),
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

    created_by = relationship(
        'User',
        back_populates='assessments',
    )
    status = relationship('AssessmentStatus')
    # TODO: Re-enable this convenience relationship which passes through the association
    # table. Disabled to enable defining AssessmentNode table in a consistent way; to
    # make this work it seems you need to use the Table() constructor, but that was
    # causing problems with constructing a relationship to Links table.
    # nodes = relationship(
    #     'Node',
    #     secondary=assessment_node,
    #     back_populates='assessments',
    # )


class Node(BaseModel):
    """The "Node Library"."""

    __tablename__ = 'node'
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    type = Column(
        Enum(NodeType),
        nullable=False,
    )
    __mapper_args__: Final[dict] = {
        'polymorphic_on': case(
            [
                (
                    type == NodeType.SOCIETAL_BENEFIT_AREA,
                    NodeTypeDiscriminator.SOCIETAL_BENEFIT_AREA,
                ),
            ],
            else_=NodeTypeDiscriminator.OTHER,
        ),
    }

    title = Column(String(128), nullable=False)
    short_name = Column(String(256), nullable=False)
    description = Column(String(512), nullable=True)

    # TODO: Implement tags!
    # tags = Column(String, nullable=False)
    # TODO: Implement versioning!
    # version = Column(String(64), nullable=True)

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

    created_by = relationship(
        'User',
        back_populates='nodes',
    )
    # TODO: Re-enable this convenience relationship which passes through the association
    # table. Disabled to enable defining AssessmentNode table in a consistent way; to
    # make this work it seems you need to use the Table() constructor, but that was
    # causing problems with constructing a relationship to Links table.
    # assessments = relationship(
    #     'Assessment',
    #     secondary=assessment_node,
    #     back_populates='nodes',
    # )


class NodeSubtypeOther(Node):
    """Fields that are used for all node types except societal benefit area."""

    __tablename__ = "node_subtype_other"
    __mapper_args__: Final[dict] = {
        'polymorphic_identity': NodeTypeDiscriminator.OTHER,
    }

    node_id = Column(
        Integer,
        ForeignKey('node.id'),
        primary_key=True,
        nullable=False,
    )

    organization = Column(String(256), nullable=False)
    funder = Column(String(256), nullable=False)
    funding_country = Column(String(256), nullable=False)
    # TODO: do we need multiple website fields?
    website = Column(String(256), nullable=True)
    contact_information = Column(String(256), nullable=False)
    persistent_identifier = Column(String(256), nullable=True)
    hypothetical = Column(Boolean, nullable=False)


class NodeSubtypeSocietalBenefitArea(Node):
    """Fields that are specific to societal benefit area type nodes."""

    __tablename__ = "node_subtype_societal_benefit_area"
    __table_args__ = (UniqueConstraint('societal_benefit_area_id'),)
    __mapper_args__: Final[dict] = {
        'polymorphic_identity': NodeTypeDiscriminator.SOCIETAL_BENEFIT_AREA,
    }

    node_id = Column(
        Integer,
        ForeignKey('node.id'),
        primary_key=True,
        nullable=False,
    )
    societal_benefit_area_id = Column(
        String,
        ForeignKey('societal_benefit_area.id'),
        nullable=False,
    )

    # TODO: Relationship to societal benefit area table? How would we make a similar
    #       relationship for the other node types?


class AssessmentNode(BaseModel):
    """An instance of a Node in the Node Library for use in an Assessment."""

    __tablename__ = "assessment_node"
    __table_args__ = (
        UniqueConstraint('assessment_id', 'node_id'),
        Index(
            f'idx_{__tablename__}',
            'assessment_id',
            'node_id',
            unique=True,  # TODO: Do we need this?
        ),
    )

    # TODO: If/when we make this a pure associative entity, do we need a surrogate ID?
    id = Column(
        Integer,
        primary_key=True,
    )
    assessment_id = Column(
        Integer,
        ForeignKey('assessment.id'),
    )
    node_id = Column(
        Integer,
        ForeignKey('node.id'),
    )

    # TODO: Special case for applications, they have performance_criteria and
    # performance_rating.

    assessment = relationship(Assessment)
    node = relationship(Node)

    input_links = relationship(
        "Link",
        foreign_keys="Link.target_assessment_node_id",
        back_populates="target_assessment_node",
    )
    output_links = relationship(
        "Link",
        foreign_keys="Link.source_assessment_node_id",
        back_populates="source_assessment_node",
    )


class Link(BaseModel):
    """A link between two nodes _in an assessment_."""

    __tablename__ = 'link'
    __table_args__ = (
        UniqueConstraint('source_assessment_node_id', 'target_assessment_node_id'),
        Index(
            f'idx_{__tablename__}',
            'source_assessment_node_id',
            'target_assessment_node_id',
            unique=True,  # TODO: Do we need this?
        ),
    )
    id = Column(
        Integer,
        autoincrement=True,
        primary_key=True,
    )
    source_assessment_node_id = Column(
        Integer,
        ForeignKey('assessment_node.id'),
        nullable=False,
    )
    target_assessment_node_id = Column(
        Integer,
        ForeignKey('assessment_node.id'),
        nullable=False,
    )

    performance_rating = Column(
        Integer,
        CheckConstraint(
            'performance_rating>0 and performance_rating<101',
            name='0-100',
        ),
        nullable=False,
    )

    source_assessment_node = relationship(
        AssessmentNode,
        foreign_keys=[source_assessment_node_id],
        back_populates='output_links',
    )
    target_assessment_node = relationship(
        AssessmentNode,
        foreign_keys=[target_assessment_node_id],
        back_populates='input_links',
    )


##################
# Reference tables
##################


# TODO: Is this "association" or "reference"
class Role(BaseModel):
    __tablename__ = 'role'
    id = Column(
        String,
        primary_key=True,
        nullable=False,
    )


class AssessmentStatus(BaseModel):
    __tablename__ = 'status'
    id = Column(
        String,
        primary_key=True,
    )
    description = Column(
        String,
        nullable=False,
    )


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
