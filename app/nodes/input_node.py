from abc import ABC
from typing import List, Tuple

import pandas as pd

from app.libs.helper import change_columns
from app.libs.parser import Parser
from app.models.file import File
from app.nodes.base_node import BaseNode


class InputNode(BaseNode, ABC):
    params = [
        Parser(name="has_header", type_=bool, description="csv是否有header", required=True)
    ]
    input_size = 0
    input_type = 0
    output_type = 1

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges, extra)
        self.header = 0 if self.has_header else None


class NotSplitInputNode(InputNode):
    description = "此节点为未拆分x,y的输入节点"
    params = [
        *InputNode.params,
        Parser(name="input_file", type_=int, description="输入文件", required=True),
        Parser(
            name="label_columns",
            type_=str,
            description="label所在列，支持多列，例如1,2:4",
            required=True,
        ),
    ]

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges, extra)
        self.input_file = File.get_by_id(self.input_file)
        assert self.input_file, "input_file not found"
        self.label_columns = change_columns(self.label_columns)

    def _run(
        self, input_files: List[List[pd.DataFrame]]
    ) -> Tuple[pd.DataFrame] or None:
        x = pd.read_csv(self.input_file.path, header=self.header)
        y = x.iloc[:, self.label_columns]
        x.drop(y.columns, axis=1, inplace=True)
        # TODO UT需要，写完填充节点后删除
        x = x.fillna(value=0)
        return x, y


class SplitInputNode(InputNode):
    description = "此节点为已拆分x,y的输入节点"
    params = [
        *InputNode.params,
        Parser(name="x_input_file", type_=int, description="x输入文件", required=True),
        Parser(name="y_input_file", type_=int, description="y输入文件", required=True),
    ]

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges, extra)
        self.x_input_file = File.get_by_id(self.x_input_file)
        assert self.x_input_file, "x_input_file not found"
        self.y_input_file = File.get_by_id(self.y_input_file)
        assert self.y_input_file, "y_input_file not found"

    def _run(
        self, input_files: List[List[pd.DataFrame]]
    ) -> Tuple[pd.DataFrame] or None:
        x = pd.read_csv(self.x_input_file.path, header=self.header)
        y = pd.read_csv(self.y_input_file.path, header=self.header)
        # TODO UT需要，写完填充节点后删除
        x = x.fillna(value=0)
        return x, y
