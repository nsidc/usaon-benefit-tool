from flask import Blueprint, Request, redirect, render_template, request, url_for
from wtforms import FormField

from usaon_vta_survey import db
from usaon_vta_survey.forms import FORMS_BY_MODEL
from usaon_vta_survey.models.tables import (
    ResponseApplication,
    ResponseDataProduct,
    ResponseDataProductApplication,
    Survey,
)
from usaon_vta_survey.util.authorization import limit_response_editors
from usaon_vta_survey.util.superform import SuperForm


def _update_super_form(
    super_form: type[SuperForm],
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
    relationship: ResponseDataProductApplication,
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
) -> ResponseDataProduct:
    """Return a data product db object (or 404)."""
    if data_product_id is not None:
        response_data_product = db.get_or_404(ResponseDataProduct, data_product_id)
    else:
        response_data_product = ResponseDataProduct(response_id=response_id)

    return response_data_product


def _response_application(
    *,
    application_id: int | None,
    response_id: int,
) -> ResponseApplication:
    """Return an application db object (or 404)."""
    if application_id is not None:
        response_application = db.get_or_404(ResponseApplication, application_id)
    else:
        response_application = ResponseApplication(response_id=response_id)

    return response_application


def _response_data_product_application(
    *,
    data_product_id: int | None,
    application_id: int | None,
) -> ResponseDataProductApplication:
    """Return a relationship db object.

    Returned object may be transient or persistent depending on whether a match exists
    in the db.
    """
    if data_product_id and application_id:
        response_data_product_application = (
            db.session.query(ResponseDataProductApplication)
            .filter(
                ResponseDataProductApplication.response_data_product_id
                == data_product_id
                and ResponseDataProductApplication.response_application_id
                == application_id
            )
            .one_or_none()
        )
    else:
        response_data_product_application = None

    if response_data_product_application is not None:
        return response_data_product_application
    else:
        return ResponseDataProductApplication()


def _request_args(request: Request) -> tuple[int | None, int | None]:
    data_product_id: int | str | None = request.args.get('data_product_id')
    if data_product_id is not None:
        data_product_id = int(data_product_id)

    application_id: int | str | None = request.args.get('application_id')
    if application_id is not None:
        application_id = int(application_id)

    return data_product_id, application_id


data_product_application_bp = Blueprint(
    'data_product_application',
    __name__,
    url_prefix='/<string:survey_id>/data_product_application_relationships',
)


@data_product_application_bp.route(
    '',
    methods=['GET', 'POST'],
)
def view_response_data_product_application_relationships(survey_id: str):
    """View and add application/dataproduct relationships to a response.

    TODO: Refactor this whole pile of stuff. Less string magic. Less cyclomatic
    complexity.
    """
    data_product_id, application_id = _request_args(request)
    survey = db.get_or_404(Survey, survey_id)

    # class SuperForm(FlaskForm):
    class ResponseDataProductApplicationForm(SuperForm):
        """Combine all necessary forms into one super-form.

        NOTE: Additional class attributes are added dynamically below.
        """

        relationship = FormField(FORMS_BY_MODEL[ResponseDataProductApplication])

    # looking for submit button at this point
    # breakpoint()
    response_data_product_application = _response_data_product_application(
        data_product_id=data_product_id,
        application_id=application_id,
    )

    response_data_product = _response_data_product(
        data_product_id=data_product_id,
        response_id=survey.response_id,
    )

    response_application = _response_application(
        application_id=application_id,
        response_id=survey.response_id,
    )

    _update_super_form(
        ResponseDataProductApplicationForm,
        data_product_id=data_product_id,
        application_id=application_id,
    )
    _update_relationship(
        response_data_product_application,
        data_product_id=data_product_id,
        application_id=application_id,
    )
    # breakpoint()

    form_obj: dict[
        str,
        ResponseDataProduct | ResponseApplication | ResponseDataProductApplication,
    ] = {
        'data_product': response_data_product,
        'application': response_application,
        # NOTE: Logic below depends on relationship being last in this dict
        'relationship': response_data_product_application,
    }

    if request.method == 'POST':
        # currently cant get here because we have no submit button
        limit_response_editors()
        form = ResponseDataProductApplicationForm(request.form, obj=form_obj)

        if form.validate():
            # Add only submitted sub-forms into the db session
            for key, obj in form_obj.items():
                if hasattr(form, key):
                    form[key].form.populate_obj(obj)
                    db.session.add(obj)

                    # Update the relationship object with the ids of any new entities
                    if type(obj) is not ResponseDataProductApplication:
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

        return redirect(
            url_for('application.view_response_applications', survey_id=survey.id)
        )

    form = ResponseDataProductApplicationForm(obj=form_obj)
    # breakpoint()
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

    # @bp.route(
    #     '/<string:survey_id>/data_product_application_relationships',
    #     methods=['GET', 'POST'],
    # )
    # def delete_response_application_societalbenefit_area_relationship(survey_id: str):
    #     """Delete application/SBA relationships to a response."""
    #     societal_benefit_area_id, application_id = _request_args(request)
    #     db.get_or_404(Survey, survey_id)

    #     return render_template(
    #         'response/relationships/data_product_application.html',
    #     )
