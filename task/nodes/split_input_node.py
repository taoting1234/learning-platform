import pandas as pd


def run(input_files, kwargs):
    x = pd.read_csv(
        "/app/files/user/{}".format(kwargs["x_input_file"]), header=kwargs["header"]
    )
    y = pd.read_csv(
        "/app/files/user/{}".format(kwargs["y_input_file"]), header=kwargs["header"]
    )
    # TODO UT需要，写完填充节点后删除
    x = x.fillna(value=0)
    return x, y
