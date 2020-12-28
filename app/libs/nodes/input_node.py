import pandas as pd

from app.libs.nodes.base_node import BaseNode
from app.models.file import File


class InputNode(BaseNode):
    allow_input = [0]

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges)
        assert len(in_edges) == 0, 'Input node cannot exist in_edges'
        # x_input_file
        x_input_file = extra.get('x_input_file')
        assert isinstance(x_input_file, int), 'x_input_file must be integer'
        self.x_input_file = File.get_by_id(x_input_file)
        assert x_input_file, 'x_input_file not found'
        # y_input_file
        y_input_file = extra.get('y_input_file')
        assert isinstance(y_input_file, int), 'y_input_file must be integer'
        self.y_input_file = File.get_by_id(y_input_file)
        assert y_input_file, 'y_input_file not found'

    @staticmethod
    def get_output(input_):
        if input_ == 0:
            return 1
        assert False

    def run(self):
        x_df = pd.read_csv(self.x_input_file.path, header=None)
        y_df = pd.read_csv(self.y_input_file.path, header=None)
        self.output_shape = [x_df.shape, y_df.shape]
        x_df.to_csv(self.join_path('x.csv'), index=False, header=False)
        y_df.to_csv(self.join_path('y.csv'), index=False, header=False)
