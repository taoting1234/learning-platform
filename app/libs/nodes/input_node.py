import pandas as pd

from app.libs.nodes.base_node import BaseNode
from app.libs.parser import Parser
from app.models.file import File


class InputNode(BaseNode):
    params = [
        Parser('x_input_file', type_=int, required=True),
        Parser('y_input_file', type_=int, required=True),
    ]
    input_node = 0
    input_size = [0]

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges, extra)
        self.x_input_file = File.get_by_id(self.x_input_file)
        assert self.x_input_file, 'x_input_file not found'
        self.y_input_file = File.get_by_id(self.y_input_file)
        assert self.y_input_file, 'y_input_file not found'
        pass

    @staticmethod
    def get_output(input_):
        return 1

    def run(self):
        x_df = pd.read_csv(self.x_input_file.path, header=None)
        y_df = pd.read_csv(self.y_input_file.path, header=None)
        self.output_shape = [x_df.shape, y_df.shape]
        x_df = x_df.fillna(value=0)
        x_df.to_csv(self.join_path('x.csv'), index=False, header=False)
        y_df.to_csv(self.join_path('y.csv'), index=False, header=False)
