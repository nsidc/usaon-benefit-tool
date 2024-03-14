from enum import Enum


# FIXME: We're inheriting from `str` to make this JSON serializable for flask-pydantic.
# Undo this once the lib fixes it.
#     https://github.com/bauerji/flask-pydantic/issues/54
class NodeType(str, Enum):
    OBSERVING_SYSTEM = 'observing_system'
    DATA_PRODUCT = 'data_product'
    APPLICATION = 'application'
    SOCIETAL_BENEFIT_AREA = 'societal_benefit_area'


class NodeTypeDiscriminator(Enum):
    OTHER = "other"
    SOCIETAL_BENEFIT_AREA = "sba"
