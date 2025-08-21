from usaon_benefit_tool._types import NodeType
from usaon_benefit_tool.models.tables import (
    NodeSubtypeOther,
    NodeSubtypeSocietalBenefitArea,
)


def get_node_class_by_type(node_type: NodeType):
    """Get the appropriate Node subclass based on `node_type`.

    This duplicates logic found in the data model, powered by a `case()` statement.

    FIXME: Dedup this logic somehow?
    """
    if node_type == NodeType.SOCIETAL_BENEFIT_AREA:
        return NodeSubtypeSocietalBenefitArea

    return NodeSubtypeOther
