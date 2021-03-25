import pickle

with open("/app/files/node/input_files.pickle", "rb") as f:
    input_files = pickle.load(f)

with open("/app/files/node/kwargs.pickle", "rb") as f:
    kwargs: dict = pickle.load(f)

func = {}
if kwargs["target"] == "nodes/custom.py":
    exec(kwargs["code"], func)
else:
    with open("/app/code/{}".format(kwargs["target"]), "r") as f:
        exec(f.read(), func)
res = func["run"](input_files, kwargs)

with open("/app/files/node/res.pickle", "wb") as f:
    pickle.dump(res, f)
