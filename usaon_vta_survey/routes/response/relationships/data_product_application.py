from flask import redirect, render_template, request, url_for

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
    """View and add application/dataproduct relationships to a response."""
    application_id = request.args.get('application_id')
    data_product_id = request.args.get('data_product_id')

    ApplicationForm = FORMS_BY_MODEL[ResponseApplication]
    DataProductForm = FORMS_BY_MODEL[ResponseDataProduct]
    DataProductApplicationForm = FORMS_BY_MODEL[ResponseDataProductApplication]

    survey = db.get_or_404(Survey, survey_id)

    if data_product_id:
        response_data_product = db.get_or_404(ResponseDataProduct, data_product_id)
    else:
        response_data_product = ResponseDataProduct(response_id=survey.response_id)

    if application_id:
        response_application = db.get_or_404(ResponseApplication, application_id)
    else:
        response_application = ResponseApplication(response_id=survey.response_id)

    if data_product_id and application_id:
        # If not found, will be `None`
        response_data_product_application = db.get(
            ResponseDataProductApplication,
            response_data_product_id,
            response_application_id,
        )
    else:
        response_data_product_application = None

    if response_data_product_application is None:
        response_data_product_application = ResponseDataProductApplication()

    if request.method == 'POST':
        # form = Form(request.form, obj=response_application)
        ...

        if form.validate():
            ...
            # form.populate_obj(response_application)
            # db.session.add(response_application)
            # db.session.commit()

        # return redirect(url_for('view_response_applications', survey_id=survey.id))
        return ...

    application_form = ApplicationForm(obj=response_application)
    data_product_form = DataProductForm(obj=response_data_product)
    relationship_form = DataProductApplicationForm(obj=response_data_product_application)
    return render_template(
        'response/relationships/data_product_application.html',
        survey=survey,
        data_product=response_data_product,
        data_products=survey.response.data_products,
        data_product_form=data_product_form,
        application=response_application,
        applications=survey.response.applications,
        application_form=application_form,
        relationship=response_data_product_application,
        relationship_form=relationship_form,
    )
