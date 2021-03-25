from lightgbm import LGBMRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor

from app.libs.parser import Parser
from app.nodes.base_node import BaseNode


class RegressorNode(BaseNode):
    target = "nodes/regressor_node.py"
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
                (
                    LinearRegression.__name__,
                    "线性回归模型",
                    "https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html",
                    [("fit_intercept", "是否计算截距", True), ("normalize", "是否归一化", False)],
                ),
                (
                    KNeighborsRegressor.__name__,
                    "KNN回归模型",
                    "https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsRegressor.html",
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
                    SVR.__name__,
                    "支持向量机回归模型",
                    "https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html",
                    [],
                ),
                (
                    RandomForestRegressor.__name__,
                    "随机森林回归模型",
                    "https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html",
                    [],
                ),
                (
                    XGBRegressor.__name__,
                    "XGB回归模型",
                    "https://xgboost.readthedocs.io/en/latest/python/python_api.html#xgboost.XGBRegressor",
                    [],
                ),
                (
                    LGBMRegressor.__name__,
                    "LGB回归模型",
                    "https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMRegressor.html",
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
