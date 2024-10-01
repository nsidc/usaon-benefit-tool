from typing import Final

from usaon_benefit_tool._types import NodeType

DUMMY_NODE_ID: Final = "__DUMMY__"

# NOTE: Each tuple is directional: `(from_node_type, to_node_type)`
ALLOWED_LINKS: Final[list[tuple[NodeType, NodeType]]] = [
    (NodeType.OBSERVING_SYSTEM, NodeType.OBSERVING_SYSTEM),
    (NodeType.OBSERVING_SYSTEM, NodeType.DATA_PRODUCT),
    (NodeType.DATA_PRODUCT, NodeType.DATA_PRODUCT),
    (NodeType.DATA_PRODUCT, NodeType.APPLICATION),
    (NodeType.APPLICATION, NodeType.APPLICATION),
    (NodeType.APPLICATION, NodeType.SOCIETAL_BENEFIT_AREA),
]
