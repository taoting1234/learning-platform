import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.neighbors import KNeighborsClassifier

from app.libs.nodes.base_node import BaseNode


class KNeighborsClassifierNode(BaseNode):
    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        super().__init__(id_, node_type, project_id, in_edges, out_edges)
        assert len(
            in_edges
        ) == 1, 'K neighbors classifier node only allow one in_edges'

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
        y_train = y_train.reshape((-1,))
        y_test = y_test.reshape((-1,))
        model = KNeighborsClassifier()
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        self.logger.info(
            'accuracy_score: {}'.format(accuracy_score(y_test, y_pred))
        )
