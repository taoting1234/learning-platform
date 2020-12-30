from app.libs.nodes.classifier_node import ClassifierNode
from app.libs.nodes.data_split_node import DataSplitNode
from app.libs.nodes.input_node import InputNode
from app.libs.nodes.regressor_node import RegressorNode

node_mapping = {
    'input_node': InputNode,
    'data_split_node': DataSplitNode,
    'regressor_node': RegressorNode,
    'classifier_node': ClassifierNode,
}
