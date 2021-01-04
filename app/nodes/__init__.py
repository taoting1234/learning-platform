from app.nodes.classifier_node import ClassifierNode
from app.nodes.custom_node import CustomNode
from app.nodes.data_split_node import DataSplitNode
from app.nodes.input_node import NotSplitInputNode, SplitInputNode
from app.nodes.regressor_node import RegressorNode

node_mapping = {
    "not_split_input_node": NotSplitInputNode,
    "split_input_node": SplitInputNode,
    "data_split_node": DataSplitNode,
    "regressor_node": RegressorNode,
    "classifier_node": ClassifierNode,
    "custom_node": CustomNode,
}
