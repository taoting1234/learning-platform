from lightgbm import LGBMRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor

from ..metric import get_metric


def run(input_files, kwargs):
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
