from itertools import chain
from typing import TypedDict

from usaon_benefit_tool.constants.sankey import DUMMY_NODE_ID
from usaon_benefit_tool.models.tables import Response, ResponseNode

# NOTE: Can't use class syntax because of hard keyword conflict "from"
HighchartsSankeySeriesLink = TypedDict(
    'HighchartsSankeySeriesLink',
    {
        "from": str,
        "to": str,
        "weight": int,
        "color": str | None,
    },
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
    series = _sankey(response)
    return series


def sankey_subset(
    response: Response,
    include_related_to_type: type[ResponseNode],
) -> HighchartsSankeySeries:
    """Provide subset of Sankey data structure.

    Include only nodes related to `include_related_to_type`.
    """
    series = _sankey(response)
    # FIXME: Using `cls.__name__` could be much better. Replace with an Enum for node
    # type.
    node_ids_matching_object_type = [
        n["id"]
        for n in series["nodes"]
        if n["type"] == include_related_to_type.__name__
    ]

    # For now, select only the outputs. That was the previous behavior, but do we like
    # it?
    filtered_links = [
        link for link in series["data"] if link["from"] in node_ids_matching_object_type
    ]

    filtered_node_ids = _node_ids_in_links(filtered_links)
    filtered_nodes = [
        node for node in series["nodes"] if node["id"] in filtered_node_ids
    ]
    return {
        "data": filtered_links,
        "nodes": filtered_nodes,
    }


def _sankey(response: Response) -> HighchartsSankeySeries:
    """Extract Sankey-relevant data from Response and format for Highcharts."""
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
            "from": _node_id(link.source),
            "to": _node_id(link.target),
            "weight": link.performance_rating,
        }
        for link in links
    ]

    series = _handle_unlinked_sankey_nodes(
        {
            "data": links_simplified,
            "nodes": nodes_simplified,
        },
    )
    return series


def _node_id(node: ResponseNode) -> str:
    """Generate a unique node id.

    The IDs of the node elements need to be made unique by adding the "type" (class
    name) as a prefix.
    """
    return f"{node.__class__.__name__}_{node.id}"


def _handle_unlinked_sankey_nodes(
    series: HighchartsSankeySeries,
) -> HighchartsSankeySeries:
    """Add a dummy link for every unlinked node.

    Highcharts doesn't show unlinked nodes, so we need to make a link to a fake node
    to display them. We set the weight to 10 for usability.

    NOTE: Tooltips are hidden in the javascript.

    See Also
    --------
        https://stackoverflow.com/questions/73033817/highcharts-sankey-node-without-links
    """
    orphan_nodes = [
        n for n in series["nodes"] if n["id"] not in _node_ids_in_links(series["data"])
    ]
    if not orphan_nodes:
        return series

    dummy_links: list[HighchartsSankeySeriesLink] = [
        {
            "from": DUMMY_NODE_ID,
            "to": n["id"],
            "weight": 10,
            "color": "transparent",
        }
        for n in orphan_nodes
    ]
    dummy_node: HighchartsSankeySeriesNode = {
        "id": DUMMY_NODE_ID,
        "name": "WARNING: Please ensure all nodes have links!",
        "type": DUMMY_NODE_ID,
        "color": "transparent",
    }
    return {
        "data": dummy_links + series["data"],
        "nodes": [dummy_node] + series["nodes"],
    }


def _node_ids_in_links(links: list[HighchartsSankeySeriesLink]) -> set[str]:
    """Get the unique node IDs present in `series["data"]`."""
    node_id_tuples = [(link["from"], link["to"]) for link in links]
    node_ids = set(chain.from_iterable(node_id_tuples))

    return node_ids
