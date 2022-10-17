from flask import redirect, render_template, url_for

from usaon_vta_survey import app, db
from usaon_vta_survey.forms import FORMS_BY_MODEL
from usaon_vta_survey.models.tables import ResponseDataProduct, Survey


@app.route('/response/<string:survey_id>/data_products', methods=['GET', 'POST'])
def view_response_data_products(survey_id: str):
    form = FORMS_BY_MODEL[ResponseDataProduct]()
    survey = db.get_or_404(Survey, survey_id)

    if form.validate_on_submit():
        response_data_product = ResponseDataProduct(
            name=form.name.data,
            response_id=survey.response.id,
            satisfaction_rating=form.satisfaction_rating.data,
        )
        db.session.add(response_data_product)
        db.session.commit()

        return redirect(url_for('view_response_data_products', survey_id=survey.id))

    return render_template(
        'response_data_products.html',
        form=form,
        survey=survey,
        response=survey.response,
        data_products=survey.response.data_products,
    )
