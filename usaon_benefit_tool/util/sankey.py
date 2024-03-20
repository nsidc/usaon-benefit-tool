from itertools import chain
from typing import NotRequired, TypedDict

from flask import render_template

from usaon_benefit_tool._types import NodeType
from usaon_benefit_tool.constants.sankey import ALLOWED_LINKS, DUMMY_NODE_ID
from usaon_benefit_tool.models.tables import Assessment, AssessmentNode, Node

# NOTE: Can't use class syntax because of hard keyword conflict "from"
HighchartsSankeySeriesLink = TypedDict(
    'HighchartsSankeySeriesLink',
    {
        "from": str,
        "to": str,
        "weight": int,
        "color": NotRequired[str],
        "id": NotRequired[int],
        "tooltipHTML": str,
    },
)


# TODO: Should we have a general function which combines permitted sources and targets?
def permitted_target_link_types(node_type: NodeType) -> set[NodeType]:
    """NodeTypes which this NodeType is permitted to link _to_."""
    return {
        *[e[1] for e in ALLOWED_LINKS if e[0] is node_type],
    }


def permitted_source_link_types(node_type: NodeType) -> set[NodeType]:
    """NodeTypes which this NodeType is permitted to link _from_."""
    return {
        *[e[0] for e in ALLOWED_LINKS if e[1] is node_type],
    }


# TODO: Use dataclasses instead
class HighchartsSankeySeriesNode(TypedDict):
    id: str
    name: str
    type: str
    color: NotRequired[str]
    tooltipHTML: str


class HighchartsSankeySeries(TypedDict):
    """Highcharts Sankey series data.

    Based on https://api.highcharts.com/highcharts/series.sankey.data
    """

    data: list[HighchartsSankeySeriesLink]
    nodes: list[HighchartsSankeySeriesNode]


# TODO: Can we do better than `object` here? Mypy doesn't correctly infer `str | int`
def sankey(assessment: Assessment) -> HighchartsSankeySeries:
    """Provide Sankey data structure, formatted for Highcharts."""
    series = _sankey(assessment)
    return series


def sankey_subset(
    assessment: Assessment,
    include_related_to_type: type[AssessmentNode],
) -> HighchartsSankeySeries:
    """Provide subset of Sankey data structure.

    Include only nodes related to `include_related_to_type`.
    """
    series = _sankey(assessment)
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


def _sankey(assessment: Assessment) -> HighchartsSankeySeries:
    """Extract Sankey-relevant data from Response and format for Highcharts.

    TODO: This is probably going to lead to lots of render calls and worse, lots of
    queries. Needs to be optimized!
    """
    assessment_nodes: list[AssessmentNode] = assessment.assessment_nodes
    nodes_simplified: list[HighchartsSankeySeriesNode] = [
        {
            "id": _node_id(an.node),
            "name": an.node.short_name,
            "type": an.node.type.value,
            "tooltipHTML": render_template(
                "partials/node_tooltip.html",
                assessment_node=an,
            ),
        }
        for an in assessment_nodes
    ]

    links = list(
        set(
            chain.from_iterable(
                [
                    *[an.input_links for an in assessment_nodes],
                    *[an.output_links for an in assessment_nodes],
                ],
            ),
        ),
    )
    links_simplified: list[HighchartsSankeySeriesLink] = [
        {
            "from": _node_id(link.source_assessment_node.node),
            "to": _node_id(link.target_assessment_node.node),
            "weight": link.criticality_rating,
            "id": link.id,
            "tooltipHTML": render_template(
                "partials/link_tooltip.html",
                link=link,
            ),
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


def _node_id(node: Node) -> str:
    """Generate a unique node id.

    The IDs of the node elements need to be made unique by adding the "type" (class
    name) as a prefix.
    """
    return f"{node.type.value}_{node.id}"


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
            "tooltipHTML": "",
        }
        for n in orphan_nodes
    ]
    dummy_node: HighchartsSankeySeriesNode = {
        "id": DUMMY_NODE_ID,
        "name": "WARNING: Please ensure all nodes have links!",
        "type": DUMMY_NODE_ID,
        "color": "transparent",
        "tooltipHTML": "",
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
