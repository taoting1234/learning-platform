import os

from app.libs.helper import change_columns
from app.libs.parser import Parser
from app.nodes.base_node import BaseNode


class InputNode(BaseNode):
    group = "输入节点"
    icon = "el-icon-upload"
    params = [Parser(name="has_header", type_=bool, description="csv是否有header", required=True)]
    input_size = 0
    input_type = 0
    output_type = 1

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges, extra)
        self.checked_params["header"] = 0 if self.checked_params["has_header"] else None


class NotSplitInputNode(InputNode):
    target = "nodes.not_split_input_node"
    name = "CSV输入节点1"
    description = "此节点为未拆分X,Y的CSV输入节点"
    params = [
        *InputNode.params,
        Parser(name="input_file", type_=str, description="输入文件", required=True),
        Parser(
            name="label_columns",
            type_=str,
            description="label所在列，支持多列，例如1,3:5代表[1,3,4]",
            required=True,
        ),
    ]

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges, extra)
        self.checked_params["label_columns"] = change_columns(self.checked_params["label_columns"])
        assert self.checked_params["input_file"][0] == "/", "input_file format error"
        self.checked_params["input_file"] = self.checked_params["input_file"][1:]
        self.checked_params["real_input_file"] = os.path.realpath(
            os.path.join(self.user_dir, self.checked_params["input_file"])
        )
        assert os.path.commonpath(
            [self.user_dir, self.checked_params["real_input_file"]]
        ) == self.user_dir or os.path.exists(self.checked_params["real_input_file"]), "file not found！"


class SplitInputNode(InputNode):
    target = "nodes.split_input_node"
    name = "CSV输入节点2"
    description = "此节点为已拆分X,Y的CSV输入节点"
    params = [
        *InputNode.params,
        Parser(name="x_input_file", type_=str, description="x输入文件", required=True),
        Parser(name="y_input_file", type_=str, description="y输入文件", required=True),
    ]

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges, extra)
        assert self.checked_params["x_input_file"][0] == "/", "x_input_file format error"
        self.checked_params["x_input_file"] = self.checked_params["x_input_file"][1:]
        self.checked_params["real_x_input_file"] = os.path.realpath(
            os.path.join(self.user_dir, self.checked_params["x_input_file"])
        )
        assert os.path.commonpath(
            [self.user_dir, self.checked_params["real_x_input_file"]]
        ) == self.user_dir or os.path.exists(self.checked_params["real_x_input_file"]), "x_input_file not found！"
        assert self.checked_params["y_input_file"][0] == "/", "y_input_file format error"
        self.checked_params["y_input_file"] = self.checked_params["y_input_file"][1:]
        self.checked_params["real_y_input_file"] = os.path.realpath(
            os.path.join(self.user_dir, self.checked_params["y_input_file"])
        )
        assert os.path.commonpath(
            [self.user_dir, self.checked_params["real_y_input_file"]]
        ) == self.user_dir or os.path.exists(self.checked_params["real_y_input_file"]), "y_input_file not found！"
