from app.libs.parser import Parser
from app.nodes.base_node import BaseNode


class DataSplitNode(BaseNode):
    target = "nodes.data_split_node"
    name = "数据切分节点"
    description = "此节点为数据切分节点，可以将数据切分为训练数据和测试数据"
    group = "数据预处理节点"
    icon = "el-icon-menu"
    params = [
        Parser(
            name="test_ratio",
            type_=float,
            description="测试集占总数据的大小",
            required=True,
            range_=(0, 1),
        ),
        Parser(name="random_state", type_=int, description="随机数种子", required=False),
    ]
    input_size = 1
    input_type = 1
    output_type = 2
