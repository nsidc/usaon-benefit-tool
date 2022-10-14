"""Forms corresponding to database models.

TODO: What can we do to improve syncing between models and forms? Consider
wtforms-sqlalchemy? Consider designing a custom class or type that can represent
everything needed to construct column and field instances, and functions for converting
objects of that class to appropriate field/column?
"""
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, TextAreaField, validators

from usaon_vta_survey.models.tables import (
    Survey,
    ResponseApplication,
    ResponseDataProduct,
    ResponseObservingSystem,
)


# Survey forms:
class SurveyForm(FlaskForm):
    notes = TextAreaField(
        'Notes',
        validators=[
            validators.DataRequired(),
            # Match length of relevant DB field:
            validators.Length(max=Survey.notes.property.columns[0].type.length),
        ],
    )


# Response entity forms:
class ObservingSystemForm(FlaskForm):
    # TODO: Support sub-types of observing systems using SelectField
    name = StringField(
        'Application name',
        validators=[
            validators.DataRequired(),
            validators.Length(max=ResponseObservingSystem.name.property.columns[0].type.length),
        ],
    )
    url = StringField(
        'URL',
        validators=[
            validators.DataRequired(),
            validators.Length(max=ResponseObservingSystem.url.property.columns[0].type.length),
        ],
    )
    author_name = StringField(
        'Author name',
        validators=[
            validators.DataRequired(),
            validators.Length(max=ResponseObservingSystem.author_name.property.columns[0].type.length),
        ],
    )
    author_email = StringField(
        'Author email',
        validators=[
            validators.DataRequired(),
            validators.Length(max=ResponseObservingSystem.author_email.property.columns[0].type.length),
        ],
    )
    funding_country = StringField(
        'Funding country',
        validators=[
            validators.DataRequired(),
            validators.Length(max=ResponseObservingSystem.funding_country.property.columns[0].type.length),
        ],
    )
    funding_agency = StringField(
        'Funding agency',
        validators=[
            validators.DataRequired(),
            validators.Length(max=ResponseObservingSystem.funding_agency.property.columns[0].type.length),
        ],
    )
    references_citations = StringField(
        'References and citations',
        validators=[
            validators.DataRequired(),
            validators.Length(max=ResponseObservingSystem.references_citations.property.columns[0].type.length),
        ],
    )
    notes = StringField(
        'Notes',
        validators=[
            validators.DataRequired(),
            validators.Length(max=ResponseObservingSystem.notes.property.columns[0].type.length),
        ],
    )


class DataProductForm(FlaskForm):
    satisfaction_rating = IntegerField(
        'Satisfaction rating (0-100)',
        validators=[
            validators.InputRequired(),
            validators.NumberRange(0, 100),
        ],
    )


class ApplicationForm(FlaskForm):
    name = StringField(
        'Application name',
        validators=[
            validators.DataRequired(),
            validators.Length(max=ResponseApplication.name.property.columns[0].type.length),
        ],
    )


# Response relationship forms:
# ...


# breakpoint()
FORMS_BY_MODEL = {
    Survey: SurveyForm,
    ResponseObservingSystem: ObservingSystemForm,
    ResponseDataProduct: DataProductForm,
    ResponseApplication: ApplicationForm,
}
