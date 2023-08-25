from flask import redirect, render_template, request, url_for
from flask_login import login_required

from usaon_vta_survey import app, db
from usaon_vta_survey.forms import FORMS_BY_MODEL
from usaon_vta_survey.models.tables import ResponseDataProduct, Survey
from usaon_vta_survey.util.authorization import limit_response_editors


@app.route('/response/<string:survey_id>/data_products', methods=['GET', 'POST'])
@login_required
def view_response_data_products(survey_id: str):
    """View and add to data products associated with a response."""
    Form = FORMS_BY_MODEL[ResponseDataProduct]
    survey = db.get_or_404(Survey, survey_id)
    response_data_product = ResponseDataProduct(response_id=survey.response_id)

    if request.method == 'POST':
        limit_response_editors()
        form = Form(request.form, obj=response_data_product)

        if form.validate():
            form.populate_obj(response_data_product)
            db.session.add(response_data_product)
            db.session.commit()

        return redirect(url_for('view_response_data_products', survey_id=survey.id))

    form = Form(obj=response_data_product)
    return render_template(
        'response/data_products.html',
        form=form,
        survey=survey,
        response=survey.response,
        data_products=survey.response.data_products,
    )
