from itertools import chain

from usaon_benefit_tool.models.tables import (
    Response,
    ResponseApplication,
    ResponseDataProduct,
    ResponseObservingSystem,
)


# TODO: Can we do better than `object` here? Mypy doesn't correctly infer `str | int`
def applications_sankey(response: Response) -> list[list[object]]:
    """Provide Sankey data structure of applications, formatted for Highcharts."""
    # Convert tuples to lists for passing to Javascript-land:
    data = [list(e) for e in _applications_sankey(response)]
    return data


def data_products_sankey(response: Response) -> list[list[object]]:
    """Provide Sankey data structure of applications, formatted for Highcharts."""
    # Convert tuples to lists for passing to Javascript-land:
    data = [list(e) for e in _data_products_sankey(response)]
    return data


def societal_benefit_areas_sankey(response: Response) -> list[list[object]]:
    """Provide Sankey data structure of applications, formatted for Highcharts."""
    # Convert tuples to lists for passing to Javascript-land:
    data = [list(e) for e in _societal_benefit_areas_sankey(response)]
    return data


def _societal_benefit_areas_sankey(response: Response):
    data = list(
        chain.from_iterable(
            [
                _application_societal_benefit_area_sankey_links(application)
                for application in response.applications
            ]
        )
    )
    return data


def _applications_sankey(response: Response) -> list[tuple[str, str, int]]:
    """Provide a sankey data structure of applications, formatted for type checker."""
    data = list(
        chain.from_iterable(
            [
                _data_product_application_sankey_links(data_product)
                for data_product in response.data_products
            ]
        )
    )
    return data


def _data_products_sankey(response: Response) -> list[tuple[str, str, int]]:
    """Provide a sankey data structure of applications, formatted for type checker."""
    data = list(
        chain.from_iterable(
            [
                _observing_system_data_product_sankey_links(observing_system)
                for observing_system in response.observing_systems
            ]
        )
    )
    return data


def _data_product_application_sankey_links(
    data_product: ResponseDataProduct,
) -> list[tuple[str, str, int]]:
    data = [
        (data_product.short_name, r.application.short_name, r.performance_rating)
        for r in data_product.output_relationships
    ]
    return data


def _observing_system_data_product_sankey_links(
    observing_system: ResponseObservingSystem,
) -> list[tuple[str, str, int]]:
    data = [
        (observing_system.short_name, r.data_product.short_name, r.performance_rating)
        for r in observing_system.output_relationships
    ]
    return data


def _application_societal_benefit_area_sankey_links(
    application: ResponseApplication,
) -> list[tuple[str, str, int]]:
    data = [
        (
            application.short_name,
            r.societal_benefit_area.societal_benefit_area_id,
            r.performance_rating,
        )
        for r in application.output_relationships
    ]
    return data
