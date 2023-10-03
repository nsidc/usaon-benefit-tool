from flask_wtf import FlaskForm
from wtforms import FormField, SubmitField


class SuperForm(FlaskForm):
    """Combine all necessary forms into one super-form.

    NOTE: Additional class attributes are added dynamically below.
    """

    relationship: FormField

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # removing CSRF token from the subform because
        # it was breaking wtforms due to csrf_token in unexpected spot
        self.relationship._fields.pop('csrf_token')
        self._cleanup_submit_buttons()

    @property
    def subforms(self) -> list:
        subforms_dict = {
            key: field
            for key, field in self._fields.items()
            if isinstance(field, FormField) and 'relationship' not in key
        }
        subforms = list(subforms_dict.values())
        return subforms

    def _cleanup_submit_buttons(self):
        """Remove all submit buttons from subforms."""
        for subform in self.subforms:
            for key, field in subform._fields.copy().items():
                if isinstance(field, SubmitField):
                    subform._fields.pop(key)
                    subform._fields.pop('csrf_token')
