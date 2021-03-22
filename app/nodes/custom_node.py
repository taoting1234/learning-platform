from app.libs.parser import Parser
from app.nodes.base_node import BaseNode

default_code = """
def run(input_files: List[List[pd.DataFrame]]) -> Tuple[pd.DataFrame]:
    x = input_files[0][0]
    y = input_files[0][1]
    print(x.describe())
    print(y.describe())
    return x, y
"""


class CustomNode(BaseNode):
    target = "nodes/custom.py"
    name = "自定义节点"
    description = "此节点为自定义节点，用户可以自行编写代码"
    group = "自定义节点"
    icon = "el-icon-question"
    params = [
        Parser(
            name="input_type",
            type_=int,
            description="输入数据类型",
            required=True,
            enum=[(0, "无数据"), (1, "未拆分训练集测试集的数据"), (2, "拆分训练集测试集的数据")],
        ),
        Parser(
            name="output_type",
            type_=int,
            description="输出数据类型",
            required=True,
            enum=[(1, "未拆分训练集测试集的数据"), (2, "拆分训练集测试集的数据")],
        ),
        Parser(
            name="code",
            type_=str,
            description="代码",
            required=True,
            default=default_code,
        ),
    ]
