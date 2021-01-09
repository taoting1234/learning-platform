import pickle

import pandas as pd
from sklearn.preprocessing import (
    MaxAbsScaler,
    MinMaxScaler,
    Normalizer,
    RobustScaler,
    StandardScaler,
)

from app.libs.parser import Parser
from app.nodes.base_node import BaseNode


class ScalerNode(BaseNode):
    description = "此节点是标准化节点，支持常见的标准化算法"
    params = [
        Parser(
            name="include_label",
            type_=bool,
            description="是否需要标准化label，对于回归问题可能有用",
            required=True,
        ),
        Parser(
            name="model",
            type_=str,
            description="标准化模型，sklearn中的模型类名称，例如StandardScaler",
            required=True,
            enum=[
                StandardScaler.__name__,
                MaxAbsScaler.__name__,
                MinMaxScaler.__name__,
                Normalizer.__name__,
                RobustScaler.__name__,
            ],
        ),
        Parser(
            name="model_kwargs",
            type_=dict,
            description="模型参数",
            required=False,
            default={},
        ),
    ]
    input_size = 1
    input_type = 2
    output_type = 2

    def run(self):
        x_train = pd.read_csv(self.join_path("x_train.csv", self.in_edges[0]))
        x_test = pd.read_csv(self.join_path("x_test.csv", self.in_edges[0]))
        y_train = pd.read_csv(self.join_path("y_train.csv", self.in_edges[0]))
        y_test = pd.read_csv(self.join_path("y_test.csv", self.in_edges[0]))
        self.input_shape = [[x_train.shape, x_test.shape, y_train.shape, y_test.shape]]
        x_columns = x_train.columns
        y_columns = y_train.columns
        x_model = globals()[self.model](**self.model_kwargs)
        x_model.fit(x_train)
        x_train = x_model.transform(x_train)
        x_test = x_model.transform(x_test)
        pickle.dump(x_model, open(self.join_path("x.model"), "rw"))
        if self.include_label:
            y_model = globals()[self.model](**self.model_kwargs)
            y_model.fit(y_train)
            y_train = y_model.transform(y_train)
            y_test = y_model.transform(y_test)
            pickle.dump(y_model, open(self.join_path("y.model"), "rw"))
        self.output_shape = [x_train.shape, x_test.shape, y_train.shape, y_test.shape]
        pd.DataFrame(x_train, columns=x_columns).to_csv(
            self.join_path("x_train.csv"), index=False
        )
        pd.DataFrame(x_test, columns=x_columns).to_csv(
            self.join_path("x_test.csv"), index=False
        )
        pd.DataFrame(y_train, columns=y_columns).to_csv(
            self.join_path("y_train.csv"), index=False
        )
        pd.DataFrame(y_test, columns=y_columns).to_csv(
            self.join_path("y_test.csv"), index=False
        )
