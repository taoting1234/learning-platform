import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR

from app.libs.metric import get_metric
from app.libs.parser import Parser
from app.nodes.base_node import BaseNode


class RegressorNode(BaseNode):
    params = [
        Parser(
            "model",
            type_=str,
            required=True,
            enum=[
                LinearRegression.__name__,
                KNeighborsRegressor.__name__,
                SVR.__name__,
            ],
        ),
        Parser("model_kwargs", type_=dict, default={}),
    ]
    input_node = 1
    input_size = [2]

    def run(self):
        x_train = pd.read_csv(
            self.join_path("x_train.csv", self.in_edges[0]), header=None
        ).to_numpy()
        x_test = pd.read_csv(
            self.join_path("x_test.csv", self.in_edges[0]), header=None
        ).to_numpy()
        y_train = pd.read_csv(
            self.join_path("y_train.csv", self.in_edges[0]), header=None
        ).to_numpy()
        y_test = pd.read_csv(
            self.join_path("y_test.csv", self.in_edges[0]), header=None
        ).to_numpy()
        model = globals()[getattr(self, "model")](**getattr(self, "model_kwargs"))
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        get_metric(self.logger, 1, y_test, y_pred)
