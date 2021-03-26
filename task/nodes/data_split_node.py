from sklearn.model_selection import train_test_split


def run(input_files, **kwargs):
    x = input_files[0][0]
    y = input_files[0][1]
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=kwargs["test_ratio"],
        random_state=kwargs["random_state"],
    )
    return x_train, x_test, y_train, y_test
