"""Forms corresponding to database models.

TODO: What can we do to improve syncing between models and forms? Consider
wtforms-sqlalchemy? Consider designing a custom class or type that can represent
everything needed to construct column and field instances, and functions for converting
objects of that class to appropriate field/column?
"""
from functools import partial

from flask_wtf import FlaskForm
from sqlalchemy.ext.declarative import DeclarativeMeta

# Figure out how to use submit fields
from wtforms import fields
from wtforms_sqlalchemy.orm import (
    ModelConverter,
    converts,
    model_form,
)

from usaon_vta_survey import db
from usaon_vta_survey.models.tables import (
    ResponseApplication,
    ResponseApplicationSocietalBenefitArea,
    ResponseDataProduct,
    ResponseDataProductApplication,
    ResponseObservingSystem,
    ResponseObservingSystemDataProduct,
    ResponseSocietalBenefitArea,
    Survey,
    User,
)

common_response_object_fields = [
    'short_name',
    'full_name',
    'organization',
    'funder',
    'funding_country',
    'website',
    'description',
    'contact_name',
    'contact_title',
    'contact_email',
    'tags',
    'version',
]

app_response_object_fields = [
    *common_response_object_fields,
    'performance_criteria',
    'performance_rating',
]


class CustomModelConverter(ModelConverter):
    @converts("String")
    def conv_String(self, field_args, **extra):
        self._string_common(field_args=field_args, **extra)
        if (
            extra['column'].type.length is not None
            and extra['column'].type.length > 256
        ):
            return fields.TextAreaField(**field_args)

        return super().conv_String(field_args, **extra)


model_form = partial(
    model_form,
    converter=CustomModelConverter(),
    db_session=db.session,
    base_class=FlaskForm,
    # submit_button=SubmitField('submit'),
)

# Workaround for missing type stubs for flask-sqlalchemy:
#     https://github.com/dropbox/sqlalchemy-stubs/issues/76#issuecomment-595839159
BaseModel: DeclarativeMeta = db.Model

FORMS_BY_MODEL: dict[BaseModel, FlaskForm] = {
    User: model_form(
        User,
        only=['orcid', 'biography', 'affiliation', 'role'],
        field_args={'role': {'get_label': 'id'}},
    ),
    Survey: model_form(Survey, only=['title', 'description']),
    # Response entities ("nodes" from Sankey diagram perspective)
    # TODO: Restrict "rating" values to correct range
    ResponseObservingSystem: model_form(
        ResponseObservingSystem,
        only=common_response_object_fields,
    ),
    ResponseDataProduct: model_form(
        ResponseDataProduct,
        only=common_response_object_fields,
    ),
    ResponseApplication: model_form(
        ResponseApplication,
        only=app_response_object_fields,
    ),
    ResponseSocietalBenefitArea: model_form(
        ResponseSocietalBenefitArea,
        only=['societal_benefit_area'],
        field_args={'societal_benefit_area': {'get_label': 'id'}},
    ),
    # Response relationships ("edges" from Sankey diagram perspective)
    ResponseObservingSystemDataProduct: model_form(
        ResponseObservingSystemDataProduct,
        only=[
            'criticality_rating',
            'performance_rating',
            'rationale',
            'needed_improvements',
        ],
    ),
    ResponseDataProductApplication: model_form(
        ResponseDataProductApplication,
        only=[
            'criticality_rating',
            'performance_rating',
            'rationale',
            'needed_improvements',
        ],
    ),
    ResponseApplicationSocietalBenefitArea: model_form(
        ResponseApplicationSocietalBenefitArea,
        only=['performance_rating'],
    ),
}
