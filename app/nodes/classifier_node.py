from typing import List, Tuple

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    BaggingClassifier,
    ExtraTreesClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
    StackingClassifier,
    VotingClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import (
    BernoulliNB,
    CategoricalNB,
    ComplementNB,
    GaussianNB,
    MultinomialNB,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from xgboost import XGBClassifier, XGBRFClassifier

from app.libs.metric import get_metric
from app.libs.parser import Parser
from app.nodes.base_node import BaseNode


class ClassifierNode(BaseNode):
    name = "机器学习分类节点"
    description = "此节点为机器学习分类节点，支持常见的分类算法"
    group = "train"
    icon = "el-icon-s-operation"
    params = [
        Parser(
            name="model",
            type_=str,
            description="模型，sklearn中的模型类名称，例如LogisticRegression",
            required=True,
            enum=[
                LogisticRegression.__name__,
                KNeighborsClassifier.__name__,
                SVC.__name__,
                LinearSVC.__name__,
                XGBClassifier.__name__,
                XGBRFClassifier.__name__,
                LGBMClassifier.__name__,
                DecisionTreeClassifier.__name__,
                ExtraTreeClassifier.__name__,
                RandomForestClassifier.__name__,
                BernoulliNB.__name__,
                CategoricalNB.__name__,
                ComplementNB.__name__,
                GaussianNB.__name__,
                MultinomialNB.__name__,
                AdaBoostClassifier.__name__,
                BaggingClassifier.__name__,
                ExtraTreesClassifier.__name__,
                GradientBoostingClassifier.__name__,
                StackingClassifier.__name__,
                VotingClassifier.__name__,
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
            get_metric(self.logger, 2, y_test, y_pred)
        else:
            get_metric(self.logger, 3, y_test, y_pred)
