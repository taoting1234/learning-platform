import importlib
import pickle
from pprint import pprint

# 获取数据
with open("/app/files/node/input_files.pickle", "rb") as f:
    input_files = pickle.load(f)
with open("/app/files/node/kwargs.pickle", "rb") as f:
    kwargs: dict = pickle.load(f)
print("kwargs: ")
pprint(kwargs)

# 运行
r = importlib.import_module(kwargs["target"])
res = r.run(input_files, **kwargs)

# 运行完成
with open("/app/files/node/res.pickle", "wb") as f:
    pickle.dump(res, f)
