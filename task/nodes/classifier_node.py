import numpy as np

from .metric import get_metric


def run(input_files, kwargs):
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
