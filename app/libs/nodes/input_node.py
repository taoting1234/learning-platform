import pandas as pd

from app.libs.nodes.base_node import BaseNode
from app.models.file import File


class InputNode(BaseNode):
    def __init__(
        self, id_, node_type, project_id, in_edges, out_edges, input_file
    ):
        super().__init__(id_, node_type, project_id, in_edges, out_edges)
        self.input_file = input_file

    def run(self):
        self.logger.debug('file id: {}'.format(self.input_file))
        if self.input_file is None:
            self.logger.error('file not found')
            raise
        file = File.get_by_id(self.input_file)
        if file is None:
            self.logger.error('file not found')
            raise
        self.logger.debug('file path: {}'.format(file.path))
        df = pd.read_csv(file.path)
        self.output_shape = df.shape
        df.to_csv(self.join_path('output.csv'))
