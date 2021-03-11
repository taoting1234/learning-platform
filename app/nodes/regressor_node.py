from typing import List, Tuple

import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    BaggingRegressor,
    ExtraTreesRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
    StackingRegressor,
    VotingRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR, LinearSVR
from sklearn.tree import ExtraTreeClassifier, ExtraTreeRegressor
from xgboost import XGBRegressor, XGBRFRegressor

from app.libs.metric import get_metric
from app.libs.parser import Parser
from app.nodes.base_node import BaseNode


class RegressorNode(BaseNode):
    name = "机器学习回归节点"
    description = "此节点为机器学习回归节点，支持常见的回归算法"
    group = "模型节点"
    icon = "el-icon-s-marketing"
    params = [
        Parser(
            name="model",
            type_=str,
            description="模型，sklearn中的模型类名称，例如LinearRegression",
            required=True,
            enum=[
                (LinearRegression.__name__, "线性回归"),
                (KNeighborsRegressor.__name__, ""),
                (SVR.__name__, ""),
                (LinearSVR.__name__, ""),
                (XGBRegressor.__name__, ""),
                (XGBRFRegressor.__name__, ""),
                (LGBMRegressor.__name__, ""),
                (ExtraTreeClassifier.__name__, ""),
                (ExtraTreeRegressor.__name__, ""),
                (RandomForestRegressor.__name__, ""),
                (AdaBoostRegressor.__name__, ""),
                (BaggingRegressor.__name__, ""),
                (ExtraTreesRegressor.__name__, ""),
                (GradientBoostingRegressor.__name__, ""),
                (StackingRegressor.__name__, ""),
                (VotingRegressor.__name__, ""),
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
    output_type = 0

    def _run(
        self, input_files: List[List[pd.DataFrame]]
    ) -> Tuple[pd.DataFrame] or None:
        x_train = input_files[0][0].to_numpy()
        x_test = input_files[0][1].to_numpy()
        y_train = input_files[0][2].to_numpy()
        y_test = input_files[0][3].to_numpy()
        y_train = y_train.reshape((-1,))
        y_test = y_test.reshape((-1,))
        model = globals()[self.model](**self.model_kwargs)
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        get_metric(self.logger, 1, y_test, y_pred)
