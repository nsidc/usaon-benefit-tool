from flask import Blueprint, Request, redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import FormField

from usaon_vta_survey import db
from usaon_vta_survey.forms import FORMS_BY_MODEL
from usaon_vta_survey.models.tables import (
    ResponseDataProduct,
    ResponseObservingSystem,
    ResponseObservingSystemDataProduct,
    Survey,
)
from usaon_vta_survey.util.authorization import limit_response_editors


def _update_super_form(
    super_form: type[FlaskForm],
    /,
    *,
    data_product_id: int | None,
    observing_system_id: int | None,
) -> None:
    """Populate the form of forms with sub-forms depending on provided IDs.

    When an ID for an object is not provided, we need to gather information from the
    user to create that object.

    TODO: Better function name.
    """
    if observing_system_id is None:
        super_form.observing_system = FormField(FORMS_BY_MODEL[ResponseObservingSystem])

    if data_product_id is None:
        super_form.data_product = FormField(FORMS_BY_MODEL[ResponseDataProduct])


def _update_relationship(
    relationship: ResponseObservingSystemDataProduct,
    *,
    observing_system_id: int | None,
    data_product_id: int | None,
) -> None:
    """Populate the relationship with any known identifiers.

    TODO: Better function name.
    """
    if observing_system_id:
        relationship.response_observing_system_id = observing_system_id

    if data_product_id:
        relationship.response_data_product_id = data_product_id


# may not need to be internal
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


def _response_observing_system(
    *,
    observing_system_id: int | None,
    response_id: int,
) -> ResponseObservingSystem:
    """Return an observing system db object (or 404)."""
    if observing_system_id is not None:
        response_observing_system = db.get_or_404(
            ResponseObservingSystem, observing_system_id
        )
    else:
        response_observing_system = ResponseObservingSystem(response_id=response_id)

    return response_observing_system


def _response_observing_system_data_product(
    *,
    observing_system_id: int | None,
    data_product_id: int | None,
) -> ResponseObservingSystemDataProduct:
    """Return a relationship db object.

    Returned object may be transient or persistent depending on whether a match exists
    in the db.
    """
    if data_product_id and observing_system_id:
        # If not found, will be `None`
        response_observing_system_data_product = (
            db.session.query(ResponseObservingSystemDataProduct)
            .filter(
                ResponseObservingSystemDataProduct.response_data_product_id
                == data_product_id
                and ResponseObservingSystemDataProduct.response_observing_system_id
                == observing_system_id
            )
            .one_or_none()
        )
    else:
        response_observing_system_data_product = None

    if response_observing_system_data_product is not None:
        return response_observing_system_data_product
    else:
        return ResponseObservingSystemDataProduct()


def _request_args(request: Request) -> tuple[int | None, int | None]:
    data_product_id: int | str | None = request.args.get('data_product_id')
    if data_product_id is not None:
        data_product_id = int(data_product_id)

    observing_system_id: int | str | None = request.args.get('observing_system_id')
    if observing_system_id is not None:
        observing_system_id = int(observing_system_id)

    return data_product_id, observing_system_id


observing_system_data_product_bp = Blueprint(
    'observing_system_data_product',
    __name__,
    url_prefix='/response/<string:survey_id>/observing_system_data_product_relationships',
)


@observing_system_data_product_bp.route(
    '',
    methods=['GET', 'POST'],
)
def view_response_observing_system_data_product_relationships(survey_id: str):
    """View and add observing system/dataproduct relationships to a response.

    TODO: Refactor this whole pile of stuff. Less string magic. Less cyclomatic
    complexity.
    """
    data_product_id, observing_system_id = _request_args(request)
    survey = db.get_or_404(Survey, survey_id)

    class SuperForm(FlaskForm):
        """Combine all necessary forms into one super-form.

        NOTE: Additional class attributes are added dynamically below.
        """

        relationship = FormField(FORMS_BY_MODEL[ResponseObservingSystemDataProduct])

    response_observing_system_data_product = _response_observing_system_data_product(
        data_product_id=data_product_id,
        observing_system_id=observing_system_id,
    )

    response_data_product = _response_data_product(
        data_product_id=data_product_id,
        response_id=survey.response_id,
    )

    response_observing_system = _response_observing_system(
        observing_system_id=observing_system_id,
        response_id=survey.response_id,
    )

    _update_super_form(
        SuperForm,
        observing_system_id=observing_system_id,
        data_product_id=data_product_id,
    )
    _update_relationship(
        response_observing_system_data_product,
        observing_system_id=observing_system_id,
        data_product_id=data_product_id,
    )

    form_obj: dict[
        str,
        ResponseObservingSystem
        | ResponseDataProduct
        | ResponseObservingSystemDataProduct,
    ] = {
        'observing_system': response_observing_system,
        'data_product': response_data_product,
        # NOTE: Logic below depends on relationship being last in this dict
        'relationship': response_observing_system_data_product,
    }

    if request.method == 'POST':
        limit_response_editors()
        form = SuperForm(request.form, obj=form_obj)

        if form.validate():
            # Add only submitted sub-forms into the db session
            for key, obj in form_obj.items():
                if hasattr(form, key):
                    form[key].form.populate_obj(obj)
                    db.session.add(obj)

                    # Update the relationship object with the ids of any new entities
                    if type(obj) is not ResponseObservingSystemDataProduct:
                        # Get the db object's new ID
                        db.session.flush()
                        db.session.refresh(obj)

                        # Update the relationship db object
                        setattr(
                            response_observing_system_data_product,
                            f'response_{key}_id',
                            obj.id,
                        )

            db.session.commit()

        return redirect(
            url_for('data_product.view_response_data_products', survey_id=survey.id)
        )

    form = SuperForm(obj=form_obj)
    return render_template(
        'response/relationships/observing_system_data_product.html',
        form=form,
        survey=survey,
        observing_system=response_observing_system,
        observing_systems=survey.response.observing_systems,
        data_product=response_data_product,
        data_products=survey.response.data_products,
        relationship=response_observing_system_data_product,
    )
