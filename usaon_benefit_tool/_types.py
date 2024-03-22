from enum import Enum


class RoleName(Enum):
    ADMIN = "admin"
    RESPONDENT = "respondent"
    ANALYST = "analyst"


# FIXME: We're inheriting from `str` to make this JSON serializable for flask-pydantic.
# Undo this once the lib fixes it.
#     https://github.com/bauerji/flask-pydantic/issues/54
class NodeType(str, Enum):
    OBSERVING_SYSTEM = 'observing_system'
    DATA_PRODUCT = 'data_product'
    APPLICATION = 'application'
    SOCIETAL_BENEFIT_AREA = 'societal_benefit_area'


class NodeTypeDiscriminator(Enum):
    # Used for both Nodes and AssessmentNodes discrimination
    OTHER = "other"  # i.e. not a special case
    SOCIETAL_BENEFIT_AREA = NodeType.SOCIETAL_BENEFIT_AREA.value

    # Used for only AssessmentNodes discrimination
    APPLICATION = NodeType.APPLICATION.value

    # Not used for any discrimination, these types have nothing special about them...
    # for now.
    # OBSERVING_SYSTEM = NodeType.OBSERVING_SYSTEM.value
    # DATA_PRODUCT = NodeType.DATA_PRODUCT.value
