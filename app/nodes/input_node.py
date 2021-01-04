import pandas as pd

from app.libs.parser import Parser
from app.models.file import File
from app.nodes.base_node import BaseNode


class InputNode(BaseNode):
    params = [Parser("has_header", type_=bool, required=True)]
    input_node = 0
    input_size = [0]

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges, extra)

    @staticmethod
    def get_output(input_):
        return 1

    def run(self):
        pass


class UnSplittedFileInputNode(InputNode):
    params = [
        Parser("x_input_file", type_=int, required=True),
        Parser("output_columns", type_=str, required=True),
    ]

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges, extra)
        self.x_input_file = File.get_by_id(self.x_input_file)
        assert self.x_input_file, "x_input_file not found"

    def run(self):
        from app.libs.helper import change_columns

        header = 0 if self.has_header else None
        x_df = pd.read_csv(self.x_input_file.path, header=header)
        columns = change_columns(self.output_columns)
        y_df = x_df[columns]
        x_df.drop(columns, axis=1, inplace=True)
        self.output_shape = [x_df.shape, y_df.shape]
        # x_df = x_df.fillna(value=0)
        x_df.to_csv(self.join_path("x.csv"), index=False)
        y_df.to_csv(self.join_path("y.csv"), index=False)


class SplittedFilesInputNode(InputNode):
    params = [
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
        header = 0 if self.has_header else None
        x_df = pd.read_csv(self.x_input_file.path, header=header)
        y_df = pd.read_csv(self.y_input_file.path, header=header)
        self.output_shape = [x_df.shape, y_df.shape]
        # x_df = x_df.fillna(value=0)
        x_df.to_csv(self.join_path("x.csv"), index=False)
        y_df.to_csv(self.join_path("y.csv"), index=False)
