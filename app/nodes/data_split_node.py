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

    def run(self):
        x_df = pd.read_csv(self.join_path("x.csv", self.in_edges[0]))
        y_df = pd.read_csv(self.join_path("y.csv", self.in_edges[0]))
        self.input_shape = [[x_df.shape, y_df.shape]]
        x_train, x_test, y_train, y_test = train_test_split(
            x_df,
            y_df,
            test_size=self.test_ratio,
            random_state=self.random_state,
        )
        self.output_shape = [x_train.shape, x_test.shape, y_train.shape, y_test.shape]
        x_train.to_csv(self.join_path("x_train.csv"), index=False)
        x_test.to_csv(self.join_path("x_test.csv"), index=False)
        y_train.to_csv(self.join_path("y_train.csv"), index=False)
        y_test.to_csv(self.join_path("y_test.csv"), index=False)
