import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, median_absolute_error

from app.libs.nodes.base_node import BaseNode


class LinearRegressionNode(BaseNode):
    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges)
        assert len(
            in_edges
        ) == 1, 'Linear regression node only allow one in_edges'

    @staticmethod
    def get_output(input_):
        if input_ == 2:
            return 2

    def run(self):
        x_train = pd.read_csv(
            self.join_path('x_train.csv', self.in_edges[0]), header=None
        )
        x_test = pd.read_csv(
            self.join_path('x_test.csv', self.in_edges[0]), header=None
        )
        y_train = pd.read_csv(
            self.join_path('y_train.csv', self.in_edges[0]), header=None
        )
        y_test = pd.read_csv(
            self.join_path('y_test.csv', self.in_edges[0]), header=None
        )
        model = LinearRegression()
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        self.logger.info('mean_absolute_error: {}'.format(mean_absolute_error(y_test, y_pred)))
        self.logger.info('mean_squared_error: {}'.format(mean_squared_error(y_test, y_pred)))
        self.logger.info('median_absolute_error: {}'.format(median_absolute_error(y_test, y_pred)))
        self.logger.info('r2_score: {}'.format(r2_score(y_test, y_pred)))
