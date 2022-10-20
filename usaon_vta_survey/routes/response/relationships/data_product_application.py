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


@app.route(
    '/response/<string:survey_id>/data_product_application_relationships',
    methods=['GET', 'POST'],
)
def view_response_data_product_application_relationships(survey_id: str):
    """View and add application/dataproduct relationships to a response.

    TODO: Refactor this whole pile of stuff.
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

    if data_product_id:
        response_data_product = db.get_or_404(ResponseDataProduct, data_product_id)
        response_data_product_application.response_data_product_id = data_product_id
    else:
        response_data_product = ResponseDataProduct(response_id=survey.response_id)
        SuperForm.data_product = FormField(FORMS_BY_MODEL[ResponseDataProduct])

    if application_id:
        response_application = db.get_or_404(ResponseApplication, application_id)
        response_data_product_application.response_application_id = application_id
    else:
        response_application = ResponseApplication(response_id=survey.response_id)
        SuperForm.application = FormField(FORMS_BY_MODEL[ResponseApplication])

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
                        db.session.flush()
                        db.session.refresh(obj)
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
