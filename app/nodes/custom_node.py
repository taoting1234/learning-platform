from app.libs.parser import Parser
from app.nodes.base_node import BaseNode


class CustomNode(BaseNode):
    params = [
        Parser(name="input_node", type_=int, description="来源节点数量", required=True),
        Parser(
            name="input_size",
            type_=list,
            description="支持的输入数据类型，0为无数据，1为未拆分训练集测试集的数据，2为拆分训练集测试集的数据",
            required=True,
        ),
        Parser(name="code", type_=str, description="代码", required=True),
    ]

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges, extra)
        for i in self.input_size:
            assert isinstance(i, int)
        self.func = {}
        exec(self.code, self.func)

    def get_output(self, input_):
        return self.func["get_output"](input_)

    def run(self):
        return self.func["run"]()
