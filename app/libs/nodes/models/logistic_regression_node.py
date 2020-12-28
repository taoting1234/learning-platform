import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)

from app.libs.nodes.base_node import BaseNode


class LogisticRegressionNode(BaseNode):
    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges)
        assert len(
            in_edges
        ) == 1, 'Logistic regression node only allow one in_edges'

    @staticmethod
    def get_output(input_):
        if input_ == 2:
            return 2

    def run(self):
        x_train = pd.read_csv(
            self.join_path('x_train.csv', self.in_edges[0]), header=None
        ).to_numpy()
        x_test = pd.read_csv(
            self.join_path('x_test.csv', self.in_edges[0]), header=None
        ).to_numpy()
        y_train = pd.read_csv(
            self.join_path('y_train.csv', self.in_edges[0]), header=None
        ).to_numpy()
        y_test = pd.read_csv(
            self.join_path('y_test.csv', self.in_edges[0]), header=None
        ).to_numpy()
        y_train = y_train.reshape((-1, ))
        y_test = y_test.reshape((-1, ))
        model = LogisticRegression(max_iter=10000)
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        self.logger.info(
            'accuracy_score: {}'.format(accuracy_score(y_test, y_pred))
        )
        self.logger.info(
            'average_precision_score: {}'.format(
                average_precision_score(y_test, y_pred)
            )
        )
        self.logger.info('f1_score: {}'.format(f1_score(y_test, y_pred)))
        self.logger.info('log_loss: {}'.format(log_loss(y_test, y_pred)))
        self.logger.info(
            'precision_score: {}'.format(precision_score(y_test, y_pred))
        )
        self.logger.info(
            'recall_score: {}'.format(recall_score(y_test, y_pred))
        )
        self.logger.info(
            'roc_auc_score: {}'.format(roc_auc_score(y_test, y_pred))
        )
