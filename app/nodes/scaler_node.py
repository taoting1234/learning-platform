from sklearn.preprocessing import MaxAbsScaler, MinMaxScaler, Normalizer, StandardScaler

from app.libs.parser import Parser
from app.nodes.base_node import BaseNode


class ScalerNode(BaseNode):
    target = "nodes/scaler_node.py"
    name = "标准化节点"
    description = "此节点是标准化节点，支持常见的标准化算法"
    group = "数据预处理节点"
    icon = "el-icon-s-data"
    params = [
        Parser(
            name="include_label",
            type_=bool,
            description="是否需要标准化label，对于回归问题可能有用",
            required=True,
        ),
        Parser(
            name="model",
            type_=str,
            description="标准化模型",
            required=True,
            enum=[
                (
                    StandardScaler.__name__,
                    "标准差标准化",
                    "https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html",
                    [],
                ),
                (
                    MaxAbsScaler.__name__,
                    "最大绝对值标准化",
                    "https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MaxAbsScaler.html",
                    [],
                ),
                (
                    MinMaxScaler.__name__,
                    "最大最小值标准化",
                    "https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html",
                    [],
                ),
                (
                    Normalizer.__name__,
                    "归一化",
                    "https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.Normalizer.html",
                    [("norm", "", "l2")],
                ),
            ],
        ),
        Parser(
            name="model_kwargs",
            type_=dict,
            description="模型参数",
            required=False,
            default={},
        ),
    ]
    input_size = 1
    input_type = 2
    output_type = 2
