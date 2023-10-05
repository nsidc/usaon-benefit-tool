from usaon_vta_survey.models.tables import Response
from usaon_vta_survey.util.sankey import (
    _applications_sankey,
    _data_products_sankey,
    _societal_benefit_areas_sankey,
)


# TODO: Can we do better than `object` here? Mypy doesn't correctly infer `str | int`
def sankey(response: Response) -> list[list[object]]:
    """Provide Sankey data structure, formatted for Highcharts."""
    # Convert tuples to lists for passing to Javascript-land:
    data = [list(e) for e in _sankey(response)]
    return data


def _sankey(response: Response) -> list[tuple[str, str, int]]:
    """Provide a sankey data structure of applications."""
    data1 = _applications_sankey(response)
    data2 = _data_products_sankey(response)
    data3 = _societal_benefit_areas_sankey(response)
    data = data1 + data2 + data3
    return data
