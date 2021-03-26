import pandas as pd


def run(input_files, **kwargs):
    x = pd.read_csv(
        "/app/files/user/{}".format(kwargs["input_file"]), header=kwargs["header"]
    )
    y = x.iloc[:, kwargs["label_columns"]]
    x.drop(y.columns, axis=1, inplace=True)
    # TODO UT需要，写完填充节点后删除
    x = x.fillna(value=0)
    return x, y
