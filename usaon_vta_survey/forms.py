from flask_wtf import FlaskForm
from wtforms import StringField, validators


# Survey forms:
class NewSurveyForm(FlaskForm):
    notes = TextAreaField(
        'Notes',
        validators=[
            validators.DataRequired(),
            # Match length of relevant DB field:
            validators.Length(max=Survey.notes.property.columns[0].type.length),
        ],
    )


# Response entity forms:
class NewApplicationForm(FlaskForm):
    name = StringField(
        'Application name',
        validators=[
            validators.DataRequired(),
            validators.Length(max=ResponseApplication.name.property.columns[0].type.length),
        ],
    )


# Response relationship forms:
# ...
