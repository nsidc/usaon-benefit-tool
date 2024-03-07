from flask import Blueprint, Request, redirect, render_template, request, url_for
from wtforms import FormField

from usaon_benefit_tool import db
from usaon_benefit_tool.forms import FORMS_BY_MODEL
from usaon_benefit_tool.models.tables import (
    Survey,
    SurveyApplication,
    SurveyApplicationSocietalBenefitArea,
    SurveySocietalBenefitArea,
)
from usaon_benefit_tool.util.authorization import limit_response_editors
from usaon_benefit_tool.util.superform import SuperForm


def _update_super_form(
    super_form: type[SuperForm],
    /,
    *,
    societal_benefit_area_id: int | None,
    application_id: int | None,
) -> None:
    """Populate the form of forms with sub-forms depending on provided IDs.

    When an ID for an object is not provided, we need to gather information from the
    user to create that object.

    TODO: Better function name.
    """
    if societal_benefit_area_id is None:
        super_form.societal_benefit_area = FormField(
            FORMS_BY_MODEL[SurveySocietalBenefitArea],
        )

    if application_id is None:
        super_form.application = FormField(FORMS_BY_MODEL[SurveyApplication])


def _update_relationship(
    relationship: SurveySocietalBenefitArea,
    *,
    societal_benefit_area_id: int | None,
    application_id: int | None,
) -> None:
    """Populate the relationship with any known identifiers.

    TODO: Better function name.
    """
    if societal_benefit_area_id:
        relationship.response_societal_benefit_area_id = societal_benefit_area_id

    if application_id:
        relationship.response_application_id = application_id


def _response_societal_benefit_area(
    *,
    societal_benefit_area_id: int | None,
    response_id: int,
) -> SurveySocietalBenefitArea:
    """Return a SBA db object (or 404)."""
    if societal_benefit_area_id is not None:
        response_societal_benefit_area = db.get_or_404(
            SurveySocietalBenefitArea,
            societal_benefit_area_id,
        )
    else:
        response_societal_benefit_area = SurveySocietalBenefitArea(
            response_id=response_id,
        )

    return response_societal_benefit_area


def _response_application(
    *,
    application_id: int | None,
    response_id: int,
) -> SurveyApplication:
    """Return an application db object (or 404)."""
    if application_id is not None:
        response_application = db.get_or_404(SurveyApplication, application_id)
    else:
        response_application = SurveyApplication(response_id=response_id)

    return response_application


def _response_application_societal_benefit_area(
    *,
    societal_benefit_area_id: int | None,
    application_id: int | None,
) -> SurveyApplicationSocietalBenefitArea:
    """Return a relationship db object.

    Returned object may be transient or persistent depending on whether a match exists
    in the db.
    """
    if societal_benefit_area_id and application_id:
        # If not found, will be `None`
        response_application_societal_benefit_area = (
            db.session.query(SurveyApplicationSocietalBenefitArea)
            .filter(
                SurveyApplicationSocietalBenefitArea.response_societal_benefit_area_id
                == societal_benefit_area_id
                and SurveyApplicationSocietalBenefitArea.response_application_id
                == application_id,
            )
            .one_or_none()
        )
    else:
        response_application_societal_benefit_area = None

    if response_application_societal_benefit_area is not None:
        return response_application_societal_benefit_area
    else:
        return SurveyApplicationSocietalBenefitArea()


def _request_args(request: Request) -> tuple[int | None, int | None]:
    societal_benefit_area_id: int | str | None = request.args.get(
        'societal_benefit_area_id',
    )
    if societal_benefit_area_id is not None:
        societal_benefit_area_id = int(societal_benefit_area_id)

    application_id: int | str | None = request.args.get('application_id')
    if application_id is not None:
        application_id = int(application_id)

    return societal_benefit_area_id, application_id


application_societal_benefit_area_bp = Blueprint(
    'application_societal_benefit_area',
    __name__,
    url_prefix='/response/<string:survey_id>/application_societal_benefit_area_relationships',
)


@application_societal_benefit_area_bp.route(
    '',
    methods=['GET', 'POST'],
)
def view_response_application_societal_benefit_area_relationships(survey_id: str):
    """View and add application/SBA relationships to a response.

    TODO: Refactor this whole pile of stuff. Less string magic. Less cyclomatic
    complexity.
    """
    societal_benefit_area_id, application_id = _request_args(request)
    survey = db.get_or_404(Survey, survey_id)

    class ApplicationSocietalBenefitAreaForm(SuperForm):
        """Combine all necessary forms into one super-form.

        NOTE: Additional class attributes are added dynamically below.
        """

        relationship = FormField(FORMS_BY_MODEL[SurveyApplicationSocietalBenefitArea])

    response_application_societal_benefit_area = (
        _response_application_societal_benefit_area(
            societal_benefit_area_id=societal_benefit_area_id,
            application_id=application_id,
        )
    )

    response_societal_benefit_area = _response_societal_benefit_area(
        societal_benefit_area_id=societal_benefit_area_id,
        response_id=survey.response_id,
    )

    response_application = _response_application(
        application_id=application_id,
        response_id=survey.response_id,
    )

    _update_super_form(
        ApplicationSocietalBenefitAreaForm,
        societal_benefit_area_id=societal_benefit_area_id,
        application_id=application_id,
    )
    _update_relationship(
        response_application_societal_benefit_area,
        societal_benefit_area_id=societal_benefit_area_id,
        application_id=application_id,
    )

    form_obj: dict[
        str,
        SurveySocietalBenefitArea
        | SurveyApplication
        | SurveyApplicationSocietalBenefitArea,
    ] = {
        'societal_benefit_area': response_societal_benefit_area,
        'application': response_application,
        # NOTE: Logic below depends on relationship being last in this dict
        'relationship': response_application_societal_benefit_area,
    }

    if request.method == 'POST':
        limit_response_editors()
        form = ApplicationSocietalBenefitAreaForm(request.form, obj=form_obj)

        if form.validate():
            # Add only submitted sub-forms into the db session
            for key, obj in form_obj.items():
                if hasattr(form, key):
                    form[key].form.populate_obj(obj)
                    db.session.add(obj)

                    # Update the relationship object with the ids of any new entities
                    if type(obj) is not SurveyApplicationSocietalBenefitArea:
                        # Get the db object's new ID
                        db.session.flush()
                        db.session.refresh(obj)

                        # Update the relationship db object
                        setattr(
                            response_application_societal_benefit_area,
                            f'response_{key}_id',
                            obj.id,
                        )

            db.session.commit()

        return redirect(url_for('sba.view_response_sbas', survey_id=survey.id))

    form = ApplicationSocietalBenefitAreaForm(obj=form_obj)
    return render_template(
        'survey/relationships/application_societal_benefit_area.html',
        form=form,
        survey=survey,
        societal_benefit_area=response_societal_benefit_area,
        societal_benefit_areas=survey.response.societal_benefit_areas,
        application=response_application,
        applications=survey.response.applications,
        relationship=response_application_societal_benefit_area,
    )


@application_societal_benefit_area_bp.route(
    '/<int:response_application_societal_benefit_area_id>',
    methods=['DELETE'],
)
def delete_response_application_societal_benefit_area_relationship(
    survey_id: int,
    response_application_societal_benefit_area_id: int,
):
    """Delete application/data product relationship."""
    survey = db.get_or_404(Survey, survey_id)
    response_application_societal_benefit_area = db.get_or_404(
        SurveyApplicationSocietalBenefitArea,
        response_application_societal_benefit_area_id,
    )
    db.session.delete(response_application_societal_benefit_area)
    db.session.commit()

    return redirect(
        url_for('sba.view_response_sbas', survey_id=survey.id),
        code=303,
    )
