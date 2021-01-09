from abc import ABC

import pandas as pd

from app.libs.parser import Parser
from app.nodes.base_node import BaseNode


class CustomNode(BaseNode, ABC):
    params = [
        Parser(
            name="input_type",
            type_=int,
            description="输入数据类型，0为无数据，1为未拆分训练集测试集的数据，2为拆分训练集测试集的数据",
            required=True,
        ),
        Parser(
            name="output_type",
            type_=int,
            description="输出数据类型，1为未拆分训练集测试集的数据，2为拆分训练集测试集的数据",
            required=True,
        ),
        Parser(name="code", type_=str, description="代码", required=True),
    ]

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges, extra)
        self.func = {}
        exec(self.code, self.func)

    def run(self):
        params = []
        for in_edge in self.in_edges:
            if self.input_type == 1:
                x = pd.read_csv(self.join_path("x.csv", in_edge))
                y = pd.read_csv(self.join_path("y.csv", in_edge))
                params.append([x, y])
                self.input_shape.append([x.shape, y.shape])
            else:
                x_train = pd.read_csv(self.join_path("x_train.csv", in_edge))
                x_test = pd.read_csv(self.join_path("x_test.csv", in_edge))
                y_train = pd.read_csv(self.join_path("y_train.csv", in_edge))
                y_test = pd.read_csv(self.join_path("y_test.csv", in_edge))
                params.append([x_train, x_test, y_train, y_test])
                self.input_shape.append(
                    [x_train.shape, x_test.shape, y_train.shape, y_test.shape]
                )
        res = self.func["run"](params)
        if self.output_type == 1:
            assert len(res) == 2
            res[0].to_csv(self.join_path("x.csv"), index=False)
            res[1].to_csv(self.join_path("y.csv"), index=False)
            self.output_shape = [res[0].shape, res[1].shape]
        else:
            assert len(res) == 4
            res[0].to_csv(self.join_path("x_train.csv"), index=False)
            res[1].to_csv(self.join_path("x_test.csv"), index=False)
            res[2].to_csv(self.join_path("y_train.csv"), index=False)
            res[3].to_csv(self.join_path("y_test.csv"), index=False)
            self.output_shape = [res[0].shape, res[1].shape, res[2].shape, res[3].shape]
