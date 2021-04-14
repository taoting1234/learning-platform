import importlib
import pickle

import numpy as np
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier


def run(input_files, **kwargs):
    x_train = input_files[0][0].to_numpy()
    x_test = input_files[0][1].to_numpy()
    y_train = input_files[0][2].to_numpy()
    y_test = input_files[0][3].to_numpy()
    y_train = y_train.reshape((-1,))
    y_test = y_test.reshape((-1,))
    model = globals()[kwargs["model"]](**kwargs["model_kwargs"])
    model.fit(x_train, y_train)
    pickle.dump(model, open("/app/files/node/x.model", "wb"))
    y_pred = model.predict(x_test)
    r = importlib.import_module("helper")
    # 判断二分类还是多分类
    if len(np.unique(y_test, return_counts=True)[0]) == 2:
        r.get_metric(2, y_test, y_pred)
    else:
        r.get_metric(3, y_test, y_pred)
