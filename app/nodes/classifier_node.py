import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
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
    input_node = 1
    input_size = [2]

    def run(self):
        x_train = pd.read_csv(
            self.join_path("x_train.csv", self.in_edges[0])
        ).to_numpy()
        x_test = pd.read_csv(self.join_path("x_test.csv", self.in_edges[0])).to_numpy()
        y_train = pd.read_csv(
            self.join_path("y_train.csv", self.in_edges[0])
        ).to_numpy()
        y_test = pd.read_csv(self.join_path("y_test.csv", self.in_edges[0])).to_numpy()
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
