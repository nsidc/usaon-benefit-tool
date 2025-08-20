from itertools import chain
from typing import NotRequired, TypedDict

from flask import render_template

from usaon_benefit_tool._types import NodeType
from usaon_benefit_tool.constants.sankey import ALLOWED_LINKS, DUMMY_NODE_ID
from usaon_benefit_tool.models.tables import Assessment, AssessmentNode, Node
from usaon_benefit_tool.util.colormap import color_for_performance_rating


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


# NOTE: Can't use class syntax because of hard keyword conflict "from". I think this
#       also means we can't use a dataclass without some workaround.
# 8-12-25: Added new fields for enhanced CSV export
HighchartsSankeySeriesLink = TypedDict(
    'HighchartsSankeySeriesLink',
    {
        "from": str,
        "to": str,
        "weight": int | float,
        "color": str,
        "id": NotRequired[int],
        "tooltipHTML": str,
        "from_name": NotRequired[str],
        "to_name": NotRequired[str],
        "performance_rating": NotRequired[int | str],
        "performance_rating_rationale": NotRequired[str],
        "criticality_rating": NotRequired[int | str],
        "critically_rating_rationale": NotRequired[str],
        "gaps_description": NotRequired[str],
    },
)


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
            # "tooltipHTML": render_template(
            #    "partials/node_tooltip.html",
            #    assessment_node=an,
            # ),
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
            "weight": _weight_for_criticality_rating(link.criticality_rating),
            "color": color_for_performance_rating(link.performance_rating),
            "id": link.id,
            "tooltipHTML": render_template(
                "partials/link_tooltip.html",
                link=link,
            ),
            "from_name": link.source_assessment_node.node.short_name,
            "to_name": link.target_assessment_node.node.short_name,
            "performance_rating": (
                link.performance_rating
                if link.performance_rating is not None
                else "unrated"
            ),
            "performance_rating_rationale": getattr(
                link,
                'performance_rating_rationale',
                '',
            )
            or '',
            "criticality_rating": (
                link.criticality_rating
                if link.criticality_rating is not None
                else "unrated"
            ),
            "critically_rating_rationale": getattr(
                link,
                'critically_rating_rationale',
                '',
            )
            or '',
            "gaps_description": getattr(link, 'gaps_description', '') or '',
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


def _weight_for_criticality_rating(criticality_rating: int | None) -> int | float:
    """If criticality rating is not set, return a very thin line."""
    if criticality_rating is None:
        return 0.5

    return criticality_rating
