from app.libs.nodes.base_node import BaseNode


class LinearRegressionNode(BaseNode):
    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges)

    @staticmethod
    def get_output(input_):
        if input_ == 2:
            return 2

    def run(self):

        pass
