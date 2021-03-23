import numpy as np
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    log_loss,
    mean_absolute_error,
    mean_squared_error,
    median_absolute_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)


def get_metric(type_, y_test, y_pred):
    metric_list = [
        [mean_absolute_error, mean_squared_error, median_absolute_error, r2_score],
        [
            accuracy_score,
            average_precision_score,
            f1_score,
            log_loss,
            precision_score,
            recall_score,
            roc_auc_score,
        ],
        [accuracy_score],
    ]
    # 1 回归 2 二分类 3 多分类
    for metric in metric_list[type_ - 1]:
        try:
            print("{}: {}".format(metric.__name__, metric(y_test, y_pred)))
        except ValueError:  # pragma: no cover
            print("{}: calculate error".format(metric.__name__))


def run(input_files, kwargs):
    from lightgbm import LGBMClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from xgboost import XGBClassifier

    x_train = input_files[0][0].to_numpy()
    x_test = input_files[0][1].to_numpy()
    y_train = input_files[0][2].to_numpy()
    y_test = input_files[0][3].to_numpy()
    y_train = y_train.reshape((-1,))
    y_test = y_test.reshape((-1,))
    model = globals()[kwargs["model"]](**kwargs["model_kwargs"])
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    # 判断二分类还是多分类
    if len(np.unique(y_test, return_counts=True)[0]) == 2:
        get_metric(2, y_test, y_pred)
    else:
        get_metric(3, y_test, y_pred)
