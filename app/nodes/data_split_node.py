from typing import List, Tuple

import pandas as pd
from sklearn.model_selection import train_test_split

from app.libs.parser import Parser
from app.nodes.base_node import BaseNode


class DataSplitNode(BaseNode):
    description = "此节点为数据切分节点，可以将数据切分为训练数据和测试数据"
    params = [
        Parser(
            name="test_ratio",
            type_=float,
            description="测试集占总数据的大小",
            required=True,
            range_=(0, 1),
        ),
        Parser(name="random_state", type_=int, description="随机数种子", required=False),
    ]
    input_size = 1
    input_type = 1
    output_type = 2

    def _run(
        self, input_files: List[List[pd.DataFrame]]
    ) -> Tuple[pd.DataFrame] or None:
        x = input_files[0][0]
        y = input_files[0][1]
        x_train, x_test, y_train, y_test = train_test_split(
            x,
            y,
            test_size=self.test_ratio,
            random_state=self.random_state,
        )
        return x_train, x_test, y_train, y_test
