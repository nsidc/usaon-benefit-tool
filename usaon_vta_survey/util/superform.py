from flask_wtf import FlaskForm
from wtforms import FormField, SubmitField


class SuperForm(FlaskForm):
    """Combine all necessary forms into one super-form.

    NOTE: Additional class attributes are added dynamically below.
    """

    relationship: FormField
    submit_button = SubmitField('submit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # removing CSRF token from the subform because
        # it was breaking wtforms due to csrf_token in unexpected spot
        self.relationship._fields.pop('csrf_token')
        self._cleanup_submit_buttons()

    @property
    def subforms(self):
        subforms = [
            field for field in self._fields.values() if isinstance(field, FormField)
        ]
        return subforms

    def _cleanup_submit_buttons(self):
        """Remove all submit buttons from subforms."""
        for subform in self.subforms:
            for key, field in subform._fields.copy().items():
                if isinstance(field, SubmitField):
                    subform._fields.pop(key)
        # TODO: generate submit_button text from list of subforms
        # self.submit_button = SubmitField('submit relationship')