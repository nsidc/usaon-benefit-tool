from flask import redirect, render_template, url_for

from usaon_vta_survey import app, db
from usaon_vta_survey.forms import FORMS_BY_MODEL
from usaon_vta_survey.models.tables import ResponseObservingSystem, Survey
from usaon_vta_survey._types import ObservingSystemType


@app.route('/response/<string:survey_id>/observing_systems', methods=['GET', 'POST'])
def view_response_observing_systems(survey_id: str):
    form = FORMS_BY_MODEL[ResponseObservingSystem]()
    survey = db.get_or_404(Survey, survey_id)

    if form.validate_on_submit():
        response_observing_system = ResponseObservingSystem(
            name=form.name.data,
            response_id=survey.response.id,
            type=ObservingSystemType.other,  # TODO: Support obs. sys. types
            url=form.url.data,
            author_name=form.author_name.data,
            author_email=form.author_email.data,
            funding_country=form.funding_country.data,
            funding_agency=form.funding_agency.data,
            references_citations=form.references_citations.data,
            notes=form.notes.data,
        )
        db.session.add(response_observing_system)
        db.session.commit()

        return redirect(url_for('view_response_observing_systems', survey_id=survey.id))

    return render_template(
        'response_observing_systems.html',
        form=form,
        survey=survey,
        response=survey.response,
        observing_systems=survey.response.observing_systems,
    )
