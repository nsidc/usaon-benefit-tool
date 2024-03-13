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
    NodeSubtypeOther,
    NodeSubtypeSocietalBenefitArea,
    User,
)

node_exclude = [
    'assessment_nodes',
    'created_by_id',
    'created_by',
    'created_timestamp',
    'updated_timestamp',
    'type',
]


class CustomModelConverter(ModelConverter):
    TEXTAREA_THRESHOLD = 256

    @converts("String")
    def conv_String(self, field_args, **extra):
        self._string_common(field_args=field_args, **extra)
        if (
            extra['column'].type.length is not None
            and extra['column'].type.length > self.TEXTAREA_THRESHOLD
        ):
            return fields.TextAreaField(**field_args)

        return super().conv_String(field_args, **extra)


model_form = partial(
    model_form,
    converter=CustomModelConverter(),
    db_session=db.session,
    base_class=FlaskForm,
)

# Workaround for missing type stubs for flask-sqlalchemy:
#     https://github.com/dropbox/sqlalchemy-stubs/issues/76#issuecomment-595839159
BaseModel: DeclarativeMeta = db.Model

FORMS_BY_MODEL: dict[BaseModel, FlaskForm] = {
    Assessment: model_form(Assessment, only=['title', 'description']),
    AssessmentNode: model_form(AssessmentNode, only=['node']),
    NodeSubtypeOther: model_form(
        NodeSubtypeOther,
        exclude=node_exclude,
    ),
    NodeSubtypeSocietalBenefitArea: model_form(
        NodeSubtypeSocietalBenefitArea,
        exclude=[*node_exclude, "societal_benefit_area_id"],
        exclude_fk=False,
    ),
    User: model_form(
        User,
        only=['orcid', 'biography', 'affiliation', 'role'],
        # Helps drop-down display the correct user-facing string
        field_args={'role': {'get_label': 'id'}},
    ),
}

# HACK: Add a submit button so bootstrap-flask's render_form macro can work
# TODO: Make this less hacky
for form in FORMS_BY_MODEL.values():
    form.submit_button = SubmitField('Submit')
