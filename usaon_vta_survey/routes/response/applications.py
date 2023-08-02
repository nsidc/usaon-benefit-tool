from flask import redirect, render_template, request, url_for

from usaon_vta_survey import app, db
from usaon_vta_survey.forms import FORMS_BY_MODEL
from usaon_vta_survey.models.tables import ResponseApplication, Survey
from usaon_vta_survey.util.authorization import limit_response_editors
from usaon_vta_survey.util.sankey import applications_sankey


@app.route('/response/<string:survey_id>/applications', methods=['GET', 'POST'])
def view_response_applications(survey_id: str):
    """View and add to applications associated with a response."""
    Form = FORMS_BY_MODEL[ResponseApplication]
    survey = db.get_or_404(Survey, survey_id)
    response_application = ResponseApplication(response_id=survey.response_id)

    if request.method == 'POST':
        limit_response_editors()
        form = Form(request.form, obj=response_application)

        if form.validate():
            form.populate_obj(response_application)
            db.session.add(response_application)
            db.session.commit()

        return redirect(url_for('view_response_applications', survey_id=survey.id))

    form = Form(obj=response_application)
    return render_template(
        'response/applications.html',
        form=form,
        survey=survey,
        response=survey.response,
        applications=survey.response.applications,
        sankey_series=applications_sankey(survey.response),
    )
