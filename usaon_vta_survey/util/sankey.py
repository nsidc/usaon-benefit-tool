from itertools import chain

from usaon_vta_survey.models.tables import Response, ResponseDataProduct


def applications_sankey(response: Response) -> list[list[str | int]]:
    """Provide Sankey data structure of applications, formatted for Highcharts."""
    # Convert tuples to lists for passing to Javascript-land:
    data = [list(e) for e in _applications_sankey(response)]
    return data


def _applications_sankey(response: Response) -> list[tuple[str, str, int]]:
    """Provide a sankey data structure of applications, formatted for type checker."""
    data = list(
        chain(
            *[
                _data_product_application_sankey_links(data_product)
                for data_product in response.data_products
            ]
        )
    )
    return data


def _data_product_application_sankey_links(
    data_product: ResponseDataProduct,
) -> list[tuple[str, str, int]]:
    data = [
        (data_product.name, r.application.name, r.performance_rating)
        for r in data_product.output_relationships
    ]
    return data
