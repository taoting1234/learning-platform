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
    from lightgbm import LGBMRegressor
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import LinearRegression
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.svm import SVR
    from xgboost import XGBRegressor

    x_train = input_files[0][0].to_numpy()
    x_test = input_files[0][1].to_numpy()
    y_train = input_files[0][2].to_numpy()
    y_test = input_files[0][3].to_numpy()
    y_train = y_train.reshape((-1,))
    y_test = y_test.reshape((-1,))
    model = globals()[kwargs["model"]](kwargs["model_kwargs"])
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    get_metric(1, y_test, y_pred)
