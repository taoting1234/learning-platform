import os

from flask import current_app

from app.libs.helper import change_columns
from app.libs.parser import Parser
from app.nodes.base_node import BaseNode


class InputNode(BaseNode):
    group = "输入节点"
    icon = "el-icon-upload"
    params = [
        Parser(name="has_header", type_=bool, description="csv是否有header", required=True)
    ]
    input_size = 0
    input_type = 0
    output_type = 1

    @property
    def user_root_dir(self):
        return os.path.realpath(
            "{}/{}/user".format(current_app.config["FILE_DIRECTORY"], self.project_id)
        )

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges, extra)
        self.checked_params["header"] = 0 if self.has_header else None
        self.header = 0 if self.has_header else None


class NotSplitInputNode(InputNode):
    target = "nodes/not_split_input_node.py"
    name = "CSV输入节点1"
    description = "此节点为未拆分x,y的csv输入节点"
    params = [
        *InputNode.params,
        Parser(name="input_file", type_=str, description="输入文件", required=True),
        Parser(
            name="label_columns",
            type_=str,
            description="label所在列，支持多列，例如1,2:4",
            required=True,
        ),
    ]

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges, extra)
        self.checked_params["label_columns"] = change_columns(self.label_columns)
        self.label_columns = change_columns(self.label_columns)
        self.input_file = os.path.realpath(
            os.path.join(self.user_root_dir, self.input_file)
        )
        assert (
            os.path.commonpath([self.user_root_dir, self.input_file])
            == self.user_root_dir
        ), "file not found！"
        assert os.path.exists(self.input_file), "file not found！"


class SplitInputNode(InputNode):
    target = "nodes/split_input_node.py"
    name = "CSV输入节点2"
    description = "此节点为已拆分x,y的csv输入节点"
    params = [
        *InputNode.params,
        Parser(name="x_input_file", type_=str, description="x输入文件", required=True),
        Parser(name="y_input_file", type_=str, description="y输入文件", required=True),
    ]

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges, extra)
        self.x_input_file = os.path.realpath(
            os.path.join(self.user_root_dir, self.x_input_file)
        )
        assert (
            os.path.commonpath([self.user_root_dir, self.x_input_file])
            == self.user_root_dir
        ), "x_file not found！"
        assert os.path.exists(self.x_input_file), "x_file not found！"
        self.y_input_file = os.path.realpath(
            os.path.join(self.user_root_dir, self.y_input_file)
        )
        assert (
            os.path.commonpath([self.user_root_dir, self.y_input_file])
            == self.user_root_dir
        ), "y_file not found！"
        assert os.path.exists(self.y_input_file), "y_file not found！"
