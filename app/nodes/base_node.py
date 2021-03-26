import os
import pickle

import docker
import pandas as pd
from flask import current_app

from app.models.node import Node


class BaseNode:
    target = ""
    name = ""
    description = ""
    group = ""
    icon = ""
    params = []
    input_size = 0  # 来源节点数量，多输入模型才会改
    input_type = 0  # 0无数据 1 未拆分训练集测试集的数据 2 拆分训练集测试集的数据
    output_type = 0
    checked_params = {}  # 参数列表

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        self.id = id_
        self.node_type = node_type
        self.project_id = project_id
        self.in_edges = in_edges
        self.out_edges = out_edges
        # shape
        self.input_shape = []
        self.output_shape = []
        # input size
        if self.__class__.__name__ != "CustomNode" and len(in_edges) != self.input_size:
            raise Exception(
                "node-{}({}) only allow {} input_size".format(
                    self.id, self.__class__.__name__, self.input_size
                )
            )
        # extra
        for param in self.params:
            param.check(extra.get(param.name))
            self.checked_params[param.name] = param.value

    def node_dir(self, id_=None):
        return "{}/{}/node/{}".format(
            current_app.config["FILE_DIRECTORY"],
            self.project_id,
            self.id if id_ is None else id_,
        )

    @property
    def user_dir(self):
        return os.path.realpath(
            "{}/{}/user".format(current_app.config["FILE_DIRECTORY"], self.project_id)
        )

    def join_path(self, filename, id_=None):
        return os.path.join(self.node_dir(id_), filename)

    def finish(self):
        self.modify(input_shape=self.input_shape, output_shape=self.output_shape)

    def modify(self, **kwargs):
        Node.get_by_id(self.id).modify(**kwargs)

    def run(self):
        # 构造输入
        input_files = []
        for in_edge in self.in_edges:
            if self.input_type == 1:
                x = pd.read_csv(self.join_path("x.csv", in_edge))
                y = pd.read_csv(self.join_path("y.csv", in_edge))
                input_files.append([x, y])
                self.input_shape.append([x.shape, y.shape])
            elif self.input_type == 2:
                x_train = pd.read_csv(self.join_path("x_train.csv", in_edge))
                x_test = pd.read_csv(self.join_path("x_test.csv", in_edge))
                y_train = pd.read_csv(self.join_path("y_train.csv", in_edge))
                y_test = pd.read_csv(self.join_path("y_test.csv", in_edge))
                input_files.append([x_train, x_test, y_train, y_test])
                self.input_shape.append(
                    [x_train.shape, x_test.shape, y_train.shape, y_test.shape]
                )
        with open(self.join_path("input_files.pickle"), "wb") as f:
            pickle.dump(input_files, f)
        with open(self.join_path("kwargs.pickle"), "wb") as f:
            self.checked_params["target"] = self.target
            pickle.dump(self.checked_params, f)
        # 运行
        current_node_path = os.path.realpath(
            "./{}/{}/node/{}".format(
                current_app.config["FILE_DIRECTORY"],
                self.project_id,
                self.id,
            )
        )
        user_file_path = self.user_dir
        code_path = os.path.realpath("task")
        volumes = {
            current_node_path: {"bind": "/app/files/node", "mode": "rw"},
            user_file_path: {"bind": "/app/files/user", "mode": "rw"},
            code_path: {"bind": "/app/code", "mode": "ro"},
        }
        if self.__class__.__name__ == "CustomNode":
            user_code_dir = self.checked_params["directory"] + "/"  # 防止被覆盖
            volumes[user_code_dir] = {"bind": "/app/user_code", "mode": "ro"}
        client = docker.from_env()
        container = client.containers.run(
            detach=True, image="taoting/learning-platform-node", volumes=volumes
        )
        container.wait()
        print(container.logs().decode())
        container.remove()
        # 解析输出
        if self.output_type == 1:
            with open(self.join_path("res.pickle"), "rb") as f:
                res = pickle.load(f)
            assert len(res) == 2
            for i in res:
                assert isinstance(i, pd.DataFrame)
            res[0].to_csv(self.join_path("x.csv"), index=False)
            res[1].to_csv(self.join_path("y.csv"), index=False)
            self.output_shape = [res[0].shape, res[1].shape]
        elif self.output_type == 2:
            with open(self.join_path("res.pickle"), "rb") as f:
                res = pickle.load(f)
            assert len(res) == 4
            for i in res:
                assert isinstance(i, pd.DataFrame)
            res[0].to_csv(self.join_path("x_train.csv"), index=False)
            res[1].to_csv(self.join_path("x_test.csv"), index=False)
            res[2].to_csv(self.join_path("y_train.csv"), index=False)
            res[3].to_csv(self.join_path("y_test.csv"), index=False)
            self.output_shape = [res[0].shape, res[1].shape, res[2].shape, res[3].shape]
