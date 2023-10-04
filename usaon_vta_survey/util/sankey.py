from usaon_vta_survey.models.tables import Response
from usaon_vta_survey.util.full_sankey import (
    _applications_sankey,
    _data_products_sankey,
    _societal_benefit_areas_sankey,
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


def societal_benefit_area_sankey(response: Response) -> list[list[object]]:
    """Provide Sankey data structure of applications, formatted for Highcharts."""
    # Convert tuples to lists for passing to Javascript-land:
    data = [list(e) for e in _societal_benefit_areas_sankey(response)]
    return data
