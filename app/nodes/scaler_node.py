import pickle
from typing import List, Tuple

import pandas as pd
from sklearn.preprocessing import MaxAbsScaler, MinMaxScaler, Normalizer, StandardScaler

from app.libs.parser import Parser
from app.nodes.base_node import BaseNode


class ScalerNode(BaseNode):
    name = "标准化节点"
    description = "此节点是标准化节点，支持常见的标准化算法"
    group = "数据预处理节点"
    icon = "el-icon-s-data"
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
            description="标准化模型",
            required=True,
            enum=[
                (
                    StandardScaler.__name__,
                    "标准差标准化",
                    "https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html",
                    [],
                ),
                (
                    MaxAbsScaler.__name__,
                    "最大绝对值标准化",
                    "https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MaxAbsScaler.html",
                    [],
                ),
                (
                    MinMaxScaler.__name__,
                    "最大最小值标准化",
                    "https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html",
                    [],
                ),
                (
                    Normalizer.__name__,
                    "归一化",
                    "https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.Normalizer.html",
                    [("norm", "", "l2")],
                ),
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

    def _run(
        self, input_files: List[List[pd.DataFrame]]
    ) -> Tuple[pd.DataFrame] or None:
        x_train = input_files[0][0]
        x_test = input_files[0][1]
        y_train = input_files[0][2]
        y_test = input_files[0][3]
        x_columns = x_train.columns
        y_columns = y_train.columns
        x_model = globals()[self.model](**self.model_kwargs)
        x_model.fit(x_train)
        x_train = x_model.transform(x_train)
        x_test = x_model.transform(x_test)
        pickle.dump(x_model, open(self.join_path("x.model"), "wb"))
        if self.include_label:
            y_model = globals()[self.model](**self.model_kwargs)
            y_model.fit(y_train)
            y_train = y_model.transform(y_train)
            y_test = y_model.transform(y_test)
            pickle.dump(y_model, open(self.join_path("y.model"), "wb"))
        return (
            pd.DataFrame(x_train, columns=x_columns),
            pd.DataFrame(x_test, columns=x_columns),
            pd.DataFrame(y_train, columns=y_columns),
            pd.DataFrame(y_test, columns=y_columns),
        )
