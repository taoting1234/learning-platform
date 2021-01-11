import pickle
from typing import List

import pandas as pd

with open("/app/files/node/input_files.pickle", "rb") as f:
    input_files: List[List[pd.DataFrame]] = pickle.load(f)

func = {}
with open("/app/files/node/custom.py", "r") as f:
    exec(f.read(), func)
res = func["run"](input_files)

with open("/app/files/node/res.pickle", "wb") as f:
    pickle.dump(res, f)
