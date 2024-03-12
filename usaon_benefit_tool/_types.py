from enum import Enum


class NodeType(Enum):
    OBSERVING_SYSTEM = 'observing_system'
    DATA_PRODUCT = 'data_product'
    APPLICATION = 'application'
    SOCIETAL_BENEFIT_AREA = 'societal_benefit_area'


class NodeTypeDiscriminator(Enum):
    OTHER = "other"
    SOCIETAL_BENEFIT_AREA = "sba"
