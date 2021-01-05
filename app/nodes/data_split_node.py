import pandas as pd
from sklearn.model_selection import train_test_split

from app.libs.parser import Parser
from app.nodes.base_node import BaseNode


class DataSplitNode(BaseNode):
    params = [
        Parser("test_ratio", type_=float, required=True, range_=(0, 1)),
        Parser("random_state", type_=int),
    ]
    input_node = 1
    input_size = [1]

    @staticmethod
    def get_output(input_):
        return 2

    def run(self):
        x_df = pd.read_csv(self.join_path("x.csv", self.in_edges[0]))
        y_df = pd.read_csv(self.join_path("y.csv", self.in_edges[0]))
        self.input_shape = [x_df.shape, y_df.shape]
        x_train, x_test, y_train, y_test = train_test_split(
            x_df,
            y_df,
            test_size=getattr(self, "test_ratio"),
            random_state=getattr(self, "random_state"),
        )
        self.output_shape = [x_train.shape, x_test.shape, y_train.shape, y_test.shape]
        x_train.to_csv(self.join_path("x_train.csv"), index=False)
        x_test.to_csv(self.join_path("x_test.csv"), index=False)
        y_train.to_csv(self.join_path("y_train.csv"), index=False)
        y_test.to_csv(self.join_path("y_test.csv"), index=False)
