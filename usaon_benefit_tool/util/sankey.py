from itertools import chain
from typing import TypedDict

from usaon_benefit_tool.models.tables import Response, ResponseNode

# NOTE: Can't use class syntax because of hard keyword conflict "from"
HighchartsSankeySeriesLink = TypedDict(
    'HighchartsSankeySeriesLink',
    {"from": str, "to": str, "weight": int},
)


# TODO: Use dataclasses instead
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
    # FIXME: Don't call this data; there's a key called "data"
    data = _sankey(response)
    return data


def sankey_subset(
    response: Response,
    include_related_to_type: type[ResponseNode],
) -> HighchartsSankeySeries:
    """Provide subset of Sankey data structure.

    Include only nodes related to `include_related_to_type`.
    """
    # FIXME: Don't call this data; there's a key called "data"
    data = _sankey(response)
    node_ids_matching_object_type = [
        n["id"] for n in data["nodes"] if n["type"] == include_related_to_type.__name__
    ]

    # For now, select only the outputs. That was the previous behavior, but do we like
    # it?
    # TODO: We may want to re-use this logic elsewhere?
    filtered_links = [
        l for l in data["data"] if l["from"] in node_ids_matching_object_type
    ]

    filtered_node_id_tuples = [(l["from"], l["to"]) for l in filtered_links]
    filtered_node_ids = set(chain.from_iterable(filtered_node_id_tuples))
    filtered_nodes = [n for n in data["nodes"] if n["id"] in filtered_node_ids]
    return {
        "data": filtered_links,
        "nodes": filtered_nodes,
    }


def _node_id(node: ResponseNode) -> str:
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
