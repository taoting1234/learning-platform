import logging
import os

from flask import current_app

from app.models.node import Node


class BaseNode:
    params = []
    input_node = 0  # 来源节点数量，多输入模型才会改
    input_size = []  # 0 无数据 1 未拆分训练集测试集的数据 2 拆分训练集测试集的数据

    def __init__(self, id_, node_type, project_id, in_edges, out_edges, extra):
        self.id = id_
        self.node_type = node_type
        self.project_id = project_id
        self.in_edges = in_edges
        self.out_edges = out_edges
        # shape
        self.input_shape = []
        self.output_shape = []
        # logger
        self.logger = logging.Logger("node-{}".format(id_))
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s %(filename)s: %(levelname)s %(message)s"
        )
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        file_handler = logging.FileHandler(self.join_path("log.txt"), mode="w")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)
        # input_node
        if len(in_edges) != self.input_node:
            raise Exception(
                "node-{}({}) only allow {} input_node".format(
                    self.id, self.__class__.__name__, self.input_node
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

    def mark_failed(self):
        node = Node.get_by_id(self.id)
        node.modify(status=3)

    def finish(self):
        node = Node.get_by_id(self.id)
        node.modify(
            input_shape=self.input_shape, output_shape=self.output_shape, status=2
        )

    @staticmethod
    def get_output(input_):
        return input_

    def run(self):  # pragma: no cover
        pass  # pragma: no cover
