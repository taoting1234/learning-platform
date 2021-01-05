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


def get_metric(logger, type_, y_test, y_pred):
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
            logger.info("{}: {}".format(metric.__name__, metric(y_test, y_pred)))
        except ValueError:
            logger.info(
                "{}: calculate error".format(metric.__name__)
            )  # pragma: no cover
