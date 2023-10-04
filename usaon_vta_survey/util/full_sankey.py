from itertools import chain

from usaon_vta_survey.models.tables import Response, ResponseDataProduct


# TODO: Can we do better than `object` here? Mypy doesn't correctly infer `str | int`
def sankey(response: Response) -> list[list[object]]:
    """Provide Sankey data structure, formatted for Highcharts."""
    # Convert tuples to lists for passing to Javascript-land:
    data = [list(e) for e in _sankey(response)]
    return data


def _sankey(response: Response) -> list[tuple[str, str, int]]:
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
        (data_product.short_name, r.application.short_name, r.performance_rating)
        for r in data_product.output_relationships
    ]
    return data
