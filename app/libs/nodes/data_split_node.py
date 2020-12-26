import pandas as pd
from sklearn.model_selection import train_test_split

from app.libs.nodes.base_node import BaseNode


class DataSplitNode(BaseNode):
    allow_input = [1]

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges)
        assert len(in_edges) == 1, 'Data split node only allow one in_edges'
        # test_ratio
        self.test_ratio = extra.get('test_ratio')
        assert isinstance(self.test_ratio, float), 'test_ratio must be float'
        assert 0 < self.test_ratio < 1, 'test_ratio must 0 < x < 1'
        # random_state
        self.random_state = extra.get('random_state')
        if self.random_state:
            assert isinstance(
                self.random_state, float
            ), 'random_state must be integer'

    @staticmethod
    def get_output(input_):
        return 2

    def run(self):
        x_df = pd.read_csv(self.join_path('x.csv', self.in_edges[0]))
        y_df = pd.read_csv(self.join_path('y.csv', self.in_edges[0]))
        x_train, x_test, y_train, y_test = train_test_split(
            x_df,
            y_df,
            test_size=self.test_ratio,
            random_state=self.random_state
        )
        x_train.to_csv('x_train.csv')
        x_test.to_csv('x_test.csv')
        y_train.to_csv('y_train.csv')
        y_test.to_csv('y_test.csv')
