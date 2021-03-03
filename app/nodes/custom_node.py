import os
import pickle
from abc import ABC
from typing import List, Tuple

import docker
import pandas as pd
from flask import current_app

from app.libs.parser import Parser
from app.nodes.base_node import BaseNode


class CustomNode(BaseNode, ABC):
    name = "自定义节点"
    description = "此节点为自定义节点，用户可以自行编写代码"
    group = "custom"
    icon = ""
    params = [
        Parser(
            name="input_type",
            type_=int,
            description="输入数据类型，0为无数据，1为未拆分训练集测试集的数据，2为拆分训练集测试集的数据",
            required=True,
        ),
        Parser(
            name="output_type",
            type_=int,
            description="输出数据类型，1为未拆分训练集测试集的数据，2为拆分训练集测试集的数据",
            required=True,
        ),
        Parser(name="code", type_=str, description="代码", required=True),
    ]

    def _run(
        self, input_files: List[List[pd.DataFrame]]
    ) -> Tuple[pd.DataFrame] or None:
        with open(self.join_path("input_files.pickle"), "wb") as f:
            pickle.dump(input_files, f)
        with open(self.join_path("custom.py"), "w") as f:
            f.write(self.code)
        client = docker.from_env()
        client.containers.run(
            image="taoting/learning-platform-node",
            auto_remove=True,
            volumes={
                os.path.realpath(
                    "./{}/{}/node/{}".format(
                        current_app.config["FILE_DIRECTORY"],
                        self.project_id,
                        self.id,
                    )
                ): {"bind": "/app/files/node", "mode": "rw"},
                os.path.realpath(
                    "./{}/{}/user".format(
                        current_app.config["FILE_DIRECTORY"], self.project_id
                    )
                ): {"bind": "/app/files/user", "mode": "ro"},
                os.path.realpath("./node_docker"): {
                    "bind": "/app/code",
                    "mode": "ro",
                },
            },
        )
        with open(self.join_path("res.pickle"), "rb") as f:
            res = pickle.load(f)
        return res
