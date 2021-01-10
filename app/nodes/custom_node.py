from abc import ABC
from typing import List, Tuple

import pandas as pd

from app.libs.parser import Parser
from app.nodes.base_node import BaseNode


class CustomNode(BaseNode, ABC):
    description = "此节点为自定义节点，用户可以自行编写代码"
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

    def _run(
        self, input_files: List[List[pd.DataFrame]]
    ) -> Tuple[pd.DataFrame] or None:
        return self.func["run"](input_files)
