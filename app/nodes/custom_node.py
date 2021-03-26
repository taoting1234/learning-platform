import os

from app.libs.parser import Parser
from app.nodes.base_node import BaseNode


class CustomNode(BaseNode):
    target = ""
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
        Parser(name="directory", type_=str, description="代码目录", required=True),
        Parser(name="target_file", type_=str, description="运行的文件", required=True),
    ]

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges, extra)
        self.input_type = self.checked_params["input_type"]
        self.output_type = self.checked_params["output_type"]
        self.target = "user." + self.checked_params["target_file"].replace(".py", "")
        assert self.checked_params["directory"][0] == "/", "directory format error"
        self.checked_params["directory"] = self.checked_params["directory"][1:]
        self.checked_params["directory"] = os.path.realpath(
            os.path.join(self.user_dir, self.checked_params["directory"])
        )
        assert os.path.commonpath(
            [self.user_dir, self.checked_params["directory"]]
        ) == self.user_dir or os.path.exists(
            self.checked_params["directory"]
        ), "directory not found！"
