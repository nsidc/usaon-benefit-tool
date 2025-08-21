"""Forms corresponding to database models."""

from functools import partial

from flask_wtf import FlaskForm
from sqlalchemy.ext.declarative import DeclarativeMeta
from wtforms import SubmitField, fields
from wtforms_sqlalchemy.orm import (
    ModelConverter,
    converts,
    model_form,
)

from usaon_benefit_tool import db
from usaon_benefit_tool.models.tables import (
    Assessment,
    AssessmentNode,
    AssessmentNodeSubtypeApplication,
    Link,
    Node,
    NodeSubtypeOther,
    NodeSubtypeSocietalBenefitArea,
    User,
)


class CustomModelConverter(ModelConverter):
    TEXTAREA_THRESHOLD = 256

    @converts("String")
    def conv_String(self, field_args, **extra):
        """Automatically use <textarea> over <input> for large string fields."""
        self._string_common(field_args=field_args, **extra)
        if (
            extra['column'].type.length is not None
            and extra['column'].type.length > self.TEXTAREA_THRESHOLD
        ):
            return fields.TextAreaField(**field_args)

        return super().conv_String(field_args, **extra)

    @converts("Boolean")
    def conv_Boolean(self, field_args, **_):
        """Prevent a required checkbox from failing client-side validation when False.

        "Unchecked" is a valid value: False!

        See: https://github.com/wtforms/wtforms-sqlalchemy/issues/47
        """
        field_args["validators"] = []
        return fields.BooleanField(**field_args)


def get_node_label(node: Node) -> str:
    return f"Object #{node.id}: {node.title}"


model_form = partial(
    model_form,
    converter=CustomModelConverter(),
    db_session=db.session,
    base_class=FlaskForm,
)

node_exclude = [
    'assessment_nodes',
    'created_by_id',
    'created_by',
    'created_timestamp',
    'updated_timestamp',
    'type',
]
assessment_node_field_args = {
    'node': {'get_label': get_node_label},
}

# Workaround for missing type stubs for flask-sqlalchemy:
#     https://github.com/dropbox/sqlalchemy-stubs/issues/76#issuecomment-595839159
BaseModel: DeclarativeMeta = db.Model

FORMS_BY_MODEL: dict[BaseModel, FlaskForm] = {
    Assessment: model_form(
        Assessment,
        only=[
            'title',
            'description',
            'hypothetical',
        ],
    ),
    AssessmentNode: model_form(
        AssessmentNode,
        only=['node'],
        field_args=assessment_node_field_args,
    ),
    AssessmentNodeSubtypeApplication: model_form(
        AssessmentNodeSubtypeApplication,
        exclude=[
            'assessment',
            'input_links',
            'output_links',
        ],
        field_args=assessment_node_field_args,
    ),
    Link: model_form(
        Link,
        field_args={
            'source_assessment_node': {'get_label': lambda an: get_node_label(an.node)},
            'target_assessment_node': {'get_label': lambda an: get_node_label(an.node)},
        },
    ),
    NodeSubtypeOther: model_form(
        NodeSubtypeOther,
        exclude=node_exclude,
    ),
    NodeSubtypeSocietalBenefitArea: model_form(
        NodeSubtypeSocietalBenefitArea,
        exclude=node_exclude,
    ),
    User: model_form(
        User,
        only=['orcid', 'biography', 'affiliation', 'role'],
        # Helps drop-down display the correct user-facing string
        field_args={'role': {'get_label': lambda role: role.id.value.title()}},
    ),
}

# HACK: Add a submit button so bootstrap-flask's render_form macro can work
# TODO: Make this less hacky
for form in FORMS_BY_MODEL.values():
    form.submit_button = SubmitField('Submit')
