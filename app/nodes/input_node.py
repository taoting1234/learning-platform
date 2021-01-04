from abc import ABC

import pandas as pd

from app.libs.helper import change_columns
from app.libs.parser import Parser
from app.models.file import File
from app.nodes.base_node import BaseNode


class InputNode(BaseNode, ABC):
    params = [Parser("has_header", type_=bool, required=True)]
    input_node = 0
    input_size = [0]

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges, extra)
        self.header = 0 if getattr(self, "has_header") else None

    @staticmethod
    def get_output(input_):
        return 1


class NotSplitInputNode(InputNode):
    params = [
        *InputNode.params,
        Parser("x_input_file", type_=int, required=True),
        Parser("output_columns", type_=str, required=True),
    ]

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges, extra)
        self.x_input_file = File.get_by_id(self.x_input_file)
        assert self.x_input_file, "x_input_file not found"
        self.output_columns = change_columns(self.output_columns)

    def run(self):
        x_df = pd.read_csv(self.x_input_file.path, header=self.header)
        y_df = x_df[self.output_columns]
        x_df.drop(self.output_columns, axis=1, inplace=True)
        self.output_shape = [x_df.shape, y_df.shape]
        # TODO UT需要，写完填充节点后删除
        x_df = x_df.fillna(value=0)
        x_df.to_csv(self.join_path("x.csv"), index=False)
        y_df.to_csv(self.join_path("y.csv"), index=False)


class SplitInputNode(InputNode):
    params = [
        *InputNode.params,
        Parser("x_input_file", type_=int, required=True),
        Parser("y_input_file", type_=int, required=True),
    ]

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges, extra)
        self.x_input_file = File.get_by_id(self.x_input_file)
        assert self.x_input_file, "x_input_file not found"
        self.y_input_file = File.get_by_id(self.y_input_file)
        assert self.y_input_file, "y_input_file not found"

    def run(self):
        x_df = pd.read_csv(self.x_input_file.path, header=self.header)
        y_df = pd.read_csv(self.y_input_file.path, header=self.header)
        self.output_shape = [x_df.shape, y_df.shape]
        # TODO UT需要，写完填充节点后删除
        x_df = x_df.fillna(value=0)
        x_df.to_csv(self.join_path("x.csv"), index=False)
        y_df.to_csv(self.join_path("y.csv"), index=False)
