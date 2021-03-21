from typing import List, Tuple

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier

from app.libs.metric import get_metric
from app.libs.parser import Parser
from app.nodes.base_node import BaseNode


class ClassifierNode(BaseNode):
    name = "机器学习分类节点"
    description = "此节点为机器学习分类节点，支持常见的分类算法"
    group = "模型节点"
    icon = "el-icon-s-operation"
    params = [
        Parser(
            name="model",
            type_=str,
            description="模型",
            required=True,
            enum=[
                (
                    LogisticRegression.__name__,
                    "逻辑回归分类",
                    "https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html",
                    [
                        ("penalty", "", "l2"),
                        ("dual", "", False),
                        ("tol", "", 1e-4),
                        ("C", "", 1.0),
                    ],
                ),
                (
                    KNeighborsClassifier.__name__,
                    "KNN分类",
                    "https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html",
                    [
                        ("n_neighbors", "邻居数量", 5),
                        ("weights", "预测中使用的权重函数", "uniform"),
                        ("algorithm", "计算KNN的算法", "auto"),
                        ("leaf_size", "", 30),
                        ("p", "", 2),
                        ("metric", "", "minkowski"),
                        ("metric_params", "", None),
                    ],
                ),
                (
                    SVC.__name__,
                    "SVC分类",
                    "https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html",
                    [],
                ),
                (
                    RandomForestClassifier.__name__,
                    "随机森林分类",
                    "https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html",
                    [],
                ),
                (
                    XGBClassifier.__name__,
                    "XGB分类",
                    "https://xgboost.readthedocs.io/en/latest/python/python_api.html#xgboost.XGBClassifier",
                    [],
                ),
                (
                    LGBMClassifier.__name__,
                    "LGB分类",
                    "https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMClassifier.html",
                    [],
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
        # 判断二分类还是多分类
        if len(np.unique(y_test, return_counts=True)[0]) == 2:
            get_metric(2, y_test, y_pred)
        else:
            get_metric(3, y_test, y_pred)
