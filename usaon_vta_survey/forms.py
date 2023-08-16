"""Forms corresponding to database models.

TODO: What can we do to improve syncing between models and forms? Consider
wtforms-sqlalchemy? Consider designing a custom class or type that can represent
everything needed to construct column and field instances, and functions for converting
objects of that class to appropriate field/column?
"""
from functools import partial

from sqlalchemy.ext.declarative import DeclarativeMeta
from wtforms import fields
from wtforms.form import Form
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


model_form = partial(model_form, converter=CustomModelConverter())
# Could do a new custom converter or add an argument to allow dropdowns
# model_form_dropdown = partial(model_form, converter=)

# Workaround for missing type stubs for flask-sqlalchemy:
#     https://github.com/dropbox/sqlalchemy-stubs/issues/76#issuecomment-595839159
BaseModel: DeclarativeMeta = db.Model

FORMS_BY_MODEL: dict[BaseModel, Form] = {
    User: model_form(
        User,
        only=['orcid', 'biography', 'affiliation', 'role_id'],
        # Allows foreign key to be included in form.
        exclude_fk=False,
    ),
    Survey: model_form(Survey, only=['title', 'notes']),
    # Response entities ("nodes" from Sankey diagram perspective)
    ResponseObservingSystem: model_form(
        ResponseObservingSystem,
        only=[
            'name',
            'url',
            'author_name',
            'author_email',
            'funding_country',
            'funding_agency',
            'references_citations',
            'notes',
        ],
    ),
    # TODO: Restrict "rating" values to correct range
    ResponseDataProduct: model_form(
        ResponseDataProduct,
        only=['name', 'performance_rating'],
    ),
    ResponseApplication: model_form(
        ResponseApplication,
        only=['name'],
    ),
    ResponseSocietalBenefitArea: model_form(
        ResponseSocietalBenefitArea,
        only=['societal_benefit_area_id'],
        exclude_fk=False,
        field_args={},
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
