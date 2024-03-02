from itertools import chain
from typing import TypedDict

from usaon_benefit_tool.models.tables import Response

# NOTE: Can't use class syntax because of hard keyword conflict "from"
HighchartsSankeySeriesLink = TypedDict(
    'HighchartsSankeySeriesLink',
    {"from": str, "to": str, "weight": int},
)


class HighchartsSankeySeriesNode(TypedDict):
    id: str
    name: str
    type: str


class HighchartsSankeySeries(TypedDict):
    """Highcharts Sankey series data.

    Based on https://api.highcharts.com/highcharts/series.sankey.data
    """

    data: list[HighchartsSankeySeriesLink]
    nodes: list[HighchartsSankeySeriesNode]


# TODO: Can we do better than `object` here? Mypy doesn't correctly infer `str | int`
def sankey(response: Response) -> HighchartsSankeySeries:
    """Provide Sankey data structure, formatted for Highcharts."""
    data = _sankey(response)
    return data


# TODO: Type of node
def _node_id(node) -> str:
    return f"{node.__class__.__name__}_{node.id}"


def _sankey(response: Response) -> HighchartsSankeySeries:
    nodes = [
        *response.observing_systems,
        *response.data_products,
        *response.applications,
        *response.societal_benefit_areas,
    ]
    nodes_simplified = [
        {
            "id": _node_id(n),
            # TODO: Need a more consistent way to access the short name
            "name": (
                n.short_name if hasattr(n, "short_name") else n.societal_benefit_area.id
            ),
            "type": n.__class__.__name__,
        }
        for n in nodes
    ]

    links = list(
        set(
            chain.from_iterable(
                [
                    *[
                        node.output_relationships
                        for node in nodes
                        if hasattr(node, "output_relationships")
                    ],
                    *[
                        node.input_relationships
                        for node in nodes
                        if hasattr(node, "input_relationships")
                    ],
                ],
            ),
        ),
    )
    links_simplified = [
        {
            "from": _node_id(l.source),
            "to": _node_id(l.target),
            "weight": l.performance_rating,
        }
        for l in links
    ]

    return {
        "data": links_simplified,
        "nodes": nodes_simplified,
    }
