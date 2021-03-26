from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier

from app.libs.parser import Parser
from app.nodes.base_node import BaseNode


class ClassifierNode(BaseNode):
    target = "nodes.classifier_node"
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
