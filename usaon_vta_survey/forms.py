"""Forms corresponding to database models.

TODO: What can we do to improve syncing between models and forms? Consider
wtforms-sqlalchemy? Consider designing a custom class or type that can represent
everything needed to construct column and field instances, and functions for converting
objects of that class to appropriate field/column?
"""
from flask_wtf import FlaskForm
from sqlalchemy.ext.declarative import DeclarativeMeta
from wtforms import IntegerField, StringField, TextAreaField, validators

from usaon_vta_survey import db
from usaon_vta_survey.models.tables import (
    ResponseApplication,
    ResponseDataProduct,
    ResponseObservingSystem,
    Survey,
)
from usaon_vta_survey.util.db.column import column_length


# Survey forms:
class SurveyForm(FlaskForm):
    notes = TextAreaField(
        'Notes',
        validators=[
            validators.DataRequired(),
            # Match length of relevant DB field:
            validators.Length(max=column_length(Survey.notes)),
        ],
    )


# Response entity forms:
class ObservingSystemForm(FlaskForm):
    # TODO: Support sub-types of observing systems using SelectField
    name = StringField(
        'Application name',
        validators=[
            validators.DataRequired(),
            validators.Length(max=column_length(ResponseObservingSystem.name)),
        ],
    )
    url = StringField(
        'URL',
        validators=[
            validators.DataRequired(),
            validators.Length(max=column_length(ResponseObservingSystem.url)),
        ],
    )
    author_name = StringField(
        'Author name',
        validators=[
            validators.DataRequired(),
            validators.Length(max=column_length(ResponseObservingSystem.author_name)),
        ],
    )
    author_email = StringField(
        'Author email',
        validators=[
            validators.DataRequired(),
            validators.Length(max=column_length(ResponseObservingSystem.author_email)),
        ],
    )
    funding_country = StringField(
        'Funding country',
        validators=[
            validators.DataRequired(),
            validators.Length(
                max=column_length(ResponseObservingSystem.funding_country)
            ),
        ],
    )
    funding_agency = StringField(
        'Funding agency',
        validators=[
            validators.DataRequired(),
            validators.Length(
                max=column_length(ResponseObservingSystem.funding_agency)
            ),
        ],
    )
    references_citations = StringField(
        'References and citations',
        validators=[
            validators.DataRequired(),
            validators.Length(
                max=column_length(ResponseObservingSystem.references_citations)
            ),
        ],
    )
    notes = StringField(
        'Notes',
        validators=[
            validators.DataRequired(),
            validators.Length(max=column_length(ResponseObservingSystem.notes)),
        ],
    )


class DataProductForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            validators.DataRequired(),
            validators.Length(max=column_length(ResponseDataProduct.name)),
        ],
    )
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
            validators.Length(max=column_length(ResponseApplication.name)),
        ],
    )


# Response relationship forms:
# ...


# Workaround for missing type stubs for flask-sqlalchemy:
#     https://github.com/dropbox/sqlalchemy-stubs/issues/76#issuecomment-595839159
BaseModel: DeclarativeMeta = db.Model

# breakpoint()
FORMS_BY_MODEL: dict[BaseModel, FlaskForm] = {
    Survey: SurveyForm,
    ResponseObservingSystem: ObservingSystemForm,
    ResponseDataProduct: DataProductForm,
    ResponseApplication: ApplicationForm,
}
