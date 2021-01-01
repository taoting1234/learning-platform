from app.nodes.classifier_node import ClassifierNode
from app.nodes.custom_node import CustomNode
from app.nodes.data_split_node import DataSplitNode
from app.nodes.input_node import InputNode
from app.nodes.regressor_node import RegressorNode

node_mapping = {
    "input_node": InputNode,
    "data_split_node": DataSplitNode,
    "regressor_node": RegressorNode,
    "classifier_node": ClassifierNode,
    "custom_node": CustomNode,
}
