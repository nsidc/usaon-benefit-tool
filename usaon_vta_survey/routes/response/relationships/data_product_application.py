from flask import redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import FormField

from usaon_vta_survey import app, db
from usaon_vta_survey.forms import FORMS_BY_MODEL
from usaon_vta_survey.models.tables import (
    ResponseApplication,
    ResponseDataProduct,
    ResponseDataProductApplication,
    Survey,
)


def _update_super_form(
    super_form: str,
    /,
    *,
    data_product_id: int | None,
    application_id: int | None,
) -> None:
    """Populate the form of forms with sub-forms depending on provided IDs.

    When an ID for an object is not provided, we need to gather information from the
    user to create that object.

    TODO: Better function name.
    """
    if data_product_id is None:
        super_form.data_product = FormField(FORMS_BY_MODEL[ResponseDataProduct])

    if application_id is None:
        super_form.application = FormField(FORMS_BY_MODEL[ResponseApplication])


def _update_relationship(
    relationship: str,
    *,
    data_product_id: int | None,
    application_id: int | None,
) -> None:
    """Populate the relationship with any known identifiers.

    TODO: Better function name.
    """
    if data_product_id:
        relationship.response_data_product_id = data_product_id

    if application_id:
        relationship.response_application_id = application_id


def _response_data_product(
    *,
    data_product_id: int | None,
    response_id: int,
) -> db.Model:
    """Return a data product db object (or 404), and do some mutations.

    TODO: Extract mutations to another function responsible for that.
    """
    if data_product_id is not None:
        response_data_product = db.get_or_404(ResponseDataProduct, data_product_id)
    else:
        response_data_product = ResponseDataProduct(response_id=response_id)

    return response_data_product


def _response_application(
    *,
    application_id: int | None,
    response_id: int,
) -> db.Model:
    """Return an application db object (or 404), and do some mutations."""
    if application_id is not None:
        response_application = db.get_or_404(ResponseApplication, application_id)
    else:
        response_application = ResponseApplication(response_id=response_id)

    return response_application


@app.route(
    '/response/<string:survey_id>/data_product_application_relationships',
    methods=['GET', 'POST'],
)
def view_response_data_product_application_relationships(survey_id: str):
    """View and add application/dataproduct relationships to a response.

    TODO: Refactor this whole pile of stuff. Less string magic. Less cyclomatic
    complexity.
    """
    application_id = request.args.get('application_id')
    data_product_id = request.args.get('data_product_id')

    survey = db.get_or_404(Survey, survey_id)

    class SuperForm(FlaskForm):
        """Combine all necessary forms into one super-form.

        NOTE: Additional class attributes are added dynamically below.
        """

        relationship = FormField(FORMS_BY_MODEL[ResponseDataProductApplication])

    if data_product_id and application_id:
        # If not found, will be `None`
        response_data_product_application = db.session.get(
            ResponseDataProductApplication,
            (data_product_id, application_id),
        )
    else:
        response_data_product_application = None

    if response_data_product_application is None:
        response_data_product_application = ResponseDataProductApplication()

    response_data_product = _response_data_product(
        data_product_id=data_product_id,
        response_id=survey.response_id,
    )

    response_application = _response_application(
        application_id=application_id,
        response_id=survey.response_id,
    )

    _update_super_form(
        SuperForm,
        data_product_id=data_product_id,
        application_id=application_id,
    )
    _update_relationship(
        response_data_product_application,
        data_product_id=data_product_id,
        application_id=application_id,
    )

    form_obj = {
        'data_product': response_data_product,
        'application': response_application,
        # NOTE: Logic below depends on relationship being last in this dict
        'relationship': response_data_product_application,
    }

    if request.method == 'POST':
        form = SuperForm(request.form, obj=form_obj)

        if form.validate():
            # Add only submitted sub-forms into the db session
            for key, obj in form_obj.items():
                if hasattr(form, key):
                    form[key].form.populate_obj(obj)
                    db.session.add(obj)

                    # Update the relationship object with the ids of any new entities
                    if key != 'relationship':
                        # Get the db object's new ID
                        db.session.flush()
                        db.session.refresh(obj)

                        # Update the relationship db object
                        setattr(
                            response_data_product_application,
                            f'response_{key}_id',
                            obj.id,
                        )

            db.session.commit()

        return redirect(url_for('view_response_applications', survey_id=survey.id))

    form = SuperForm(obj=form_obj)
    return render_template(
        'response/relationships/data_product_application.html',
        form=form,
        survey=survey,
        data_product=response_data_product,
        data_products=survey.response.data_products,
        application=response_application,
        applications=survey.response.applications,
        relationship=response_data_product_application,
    )
