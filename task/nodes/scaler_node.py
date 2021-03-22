import pickle

import pandas as pd
from sklearn.preprocessing import MaxAbsScaler, MinMaxScaler, Normalizer, StandardScaler


def run(input_files, kwargs):
    x_train = input_files[0][0]
    x_test = input_files[0][1]
    y_train = input_files[0][2]
    y_test = input_files[0][3]
    x_columns = x_train.columns
    y_columns = y_train.columns
    x_model = globals()[kwargs["model"]](**kwargs["model_kwargs"])
    x_model.fit(x_train)
    x_train = x_model.transform(x_train)
    x_test = x_model.transform(x_test)
    pickle.dump(x_model, open("x.model", "wb"))
    if kwargs["include_label"]:
        y_model = globals()[kwargs["model"]](**kwargs["model_kwargs"])
        y_model.fit(y_train)
        y_train = y_model.transform(y_train)
        y_test = y_model.transform(y_test)
        pickle.dump(y_model, open("y.model", "wb"))
    return (
        pd.DataFrame(x_train, columns=x_columns),
        pd.DataFrame(x_test, columns=x_columns),
        pd.DataFrame(y_train, columns=y_columns),
        pd.DataFrame(y_test, columns=y_columns),
    )
