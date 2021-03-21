import os
from abc import abstractmethod
from typing import List, Tuple

import pandas as pd
from flask import current_app

from app.models.node import Node


class BaseNode:
    name = ""
    description = ""
    group = ""
    icon = ""
    params = []
    input_size = 0  # 来源节点数量，多输入模型才会改
    input_type = 0  # 0无数据 1 未拆分训练集测试集的数据 2 拆分训练集测试集的数据
    output_type = 0

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
            setattr(self, param.name, param.value)

    def dictionary_path(self, id_=None):
        return "{}/{}/node/{}".format(
            current_app.config["FILE_DIRECTORY"],
            self.project_id,
            self.id if id_ is None else id_,
        )

    def join_path(self, filename, id_=None):
        return os.path.join(self.dictionary_path(id_), filename)

    def finish(self):
        self.modify(input_shape=self.input_shape, output_shape=self.output_shape)

    def modify(self, **kwargs):
        Node.get_by_id(self.id).modify(**kwargs)

    @abstractmethod
    def _run(
        self, input_files: List[List[pd.DataFrame]]
    ) -> Tuple[pd.DataFrame] or None:  # pragma: no cover
        raise NotImplementedError

    def run(self) -> None:
        params = []
        for in_edge in self.in_edges:
            if self.input_type == 1:
                x = pd.read_csv(self.join_path("x.csv", in_edge))
                y = pd.read_csv(self.join_path("y.csv", in_edge))
                params.append([x, y])
                self.input_shape.append([x.shape, y.shape])
            elif self.input_type == 2:
                x_train = pd.read_csv(self.join_path("x_train.csv", in_edge))
                x_test = pd.read_csv(self.join_path("x_test.csv", in_edge))
                y_train = pd.read_csv(self.join_path("y_train.csv", in_edge))
                y_test = pd.read_csv(self.join_path("y_test.csv", in_edge))
                params.append([x_train, x_test, y_train, y_test])
                self.input_shape.append(
                    [x_train.shape, x_test.shape, y_train.shape, y_test.shape]
                )
        res = self._run(params)
        if self.output_type == 1:
            assert len(res) == 2
            for i in res:
                assert isinstance(i, pd.DataFrame)
            res[0].to_csv(self.join_path("x.csv"), index=False)
            res[1].to_csv(self.join_path("y.csv"), index=False)
            self.output_shape = [res[0].shape, res[1].shape]
        elif self.output_type == 2:
            assert len(res) == 4
            for i in res:
                assert isinstance(i, pd.DataFrame)
            res[0].to_csv(self.join_path("x_train.csv"), index=False)
            res[1].to_csv(self.join_path("x_test.csv"), index=False)
            res[2].to_csv(self.join_path("y_train.csv"), index=False)
            res[3].to_csv(self.join_path("y_test.csv"), index=False)
            self.output_shape = [res[0].shape, res[1].shape, res[2].shape, res[3].shape]
