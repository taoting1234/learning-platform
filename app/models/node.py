import json
import os
from threading import Thread

from flask import current_app
from sqlalchemy import Column, ForeignKey, Integer, String

from app.libs.global_varible import g
from app.models.base import Base
from app.models.project import Project


class Node(Base):
    __tablename__ = "node"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey(Project.id), nullable=False)
    node_type = Column(String(100), nullable=False)
    _input_shape = Column("input_shape", String(1000), default="[]", nullable=False)
    _output_shape = Column("output_shape", String(1000), default="[]", nullable=False)
    _in_edges = Column("in_edges", String(1000), default="[]", nullable=False)
    _out_edges = Column("out_edge", String(1000), default="[]", nullable=False)
    status = Column(Integer, default=0, nullable=False)  # 0 未运行 1 正在运行 2 运行完成 3 运行失败
    _extra = Column("extra", String(1000), default="{}", nullable=False)

    @property
    def input_shape(self):
        return json.loads(self._input_shape)

    @input_shape.setter
    def input_shape(self, raw):
        self._input_shape = json.dumps(raw)

    @property
    def output_shape(self):
        return json.loads(self._output_shape)

    @output_shape.setter
    def output_shape(self, raw):
        self._output_shape = json.dumps(raw)

    @property
    def in_edges(self):
        return json.loads(self._in_edges)

    @in_edges.setter
    def in_edges(self, raw):
        self._in_edges = json.dumps(raw)

    @property
    def out_edges(self):
        return json.loads(self._out_edges)

    @out_edges.setter
    def out_edges(self, raw):
        self._out_edges = json.dumps(raw)

    @property
    def extra(self):
        return json.loads(self._extra)

    @extra.setter
    def extra(self, raw):
        self._extra = json.dumps(raw)

    @property
    def dictionary_path(self):
        return "{}/{}/node/{}".format(
            current_app.config["FILE_DIRECTORY"], self.project_id, self.id
        )

    def join_path(self, filename):
        return os.path.join(self.dictionary_path, filename)

    @property
    def log(self):
        if os.path.exists(self.join_path("log.txt")):
            with open(self.join_path("log.txt")) as f:
                return f.read()

    @classmethod
    def create(cls, **kwargs):
        base = super().create(**kwargs)
        os.makedirs(
            "{}/{}/node/{}".format(
                current_app.config["FILE_DIRECTORY"], base.project_id, base.id
            ),
            exist_ok=True,
        )
        return base

    def delete(self):
        nodes = Node.search(project_id=self.project_id, page_size=-1)["data"]
        for node in nodes:
            if self.id in node.in_edges:
                in_edges = node.in_edges.copy()
                in_edges.remove(self.id)
                node.modify(in_edges=in_edges)
            if self.id in node.out_edges:
                out_edges = node.out_edges.copy()
                out_edges.remove(self.id)
                node.modify(out_edges=out_edges)
        super().delete()

    def run(self, only_check=False):
        from app.libs.helper import run_nodes

        nodes = self.get_nodes(self)
        nodes = self.change_nodes(nodes)
        input_ = 0
        for node in nodes:
            if input_ not in node.input_size:
                raise Exception(
                    "Node{}({}) not support input {}".format(
                        node.id, node.node_type, input_
                    )
                )
            input_ = node.get_output(input_)
        if only_check:
            return  # pragma: no cover
        for node in nodes:
            node.modify(status=1)  # 运行中
        if current_app.config["TESTING"] and not current_app.config.get("THREAD"):
            run_nodes(nodes, True, False)
        else:
            t = Thread(
                target=run_nodes,
                args=(
                    nodes,
                    current_app.config["TESTING"],
                    current_app.config.get("THREAD"),
                ),
            )
            t.start()
            if current_app.config["TESTING"]:
                if getattr(g, "thread_list", None) is None:
                    g.thread_list = []
                g.thread_list.append(t)

    @staticmethod
    def get_nodes(node, type_=1):  # 1前序节点 2后序节点
        res = []
        nodes = [node]
        while nodes:
            node = nodes.pop()
            if node in res:
                raise Exception("Graph have cycle")
            res.append(node)
            if type_ == 1:
                for node_id in node.in_edges:
                    nodes.append(Node.get_by_id(node_id))
            else:
                for node_id in node.out_edges:
                    nodes.append(Node.get_by_id(node_id))
        if type_ == 1:
            res.reverse()
        return res

    @staticmethod
    def change_nodes(nodes):
        from app.libs.helper import change_node

        res = []
        for node in nodes:
            res.append(change_node(node))
        return res

    def __eq__(self, other):
        return isinstance(other, Node) and self.id == other.id
