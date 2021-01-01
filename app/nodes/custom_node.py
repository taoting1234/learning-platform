from app.libs.parser import Parser
from app.nodes.base_node import BaseNode


class CustomNode(BaseNode):
    params = [
        Parser("input_node", type_=int, required=True),
        Parser("input_size", type_=list, required=True),
        Parser("get_output_code", type_=str, required=True),
        Parser("run_code", type_=str, required=True),
    ]

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges, extra)
        for i in self.input_size:
            assert isinstance(i, int)
        self.func = {}
        exec(getattr(self, "get_output_code"), self.func)
        exec(getattr(self, "run_code"), self.func)

    def get_output(self, input_):
        return self.func["get_output"](input_)

    def run(self):
        return self.func["run"]()
