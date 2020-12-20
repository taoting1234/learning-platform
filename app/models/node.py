import json
import os

from sqlalchemy import Column, ForeignKey, Integer, String

from app.models.base import Base
from app.models.project import Project


class Node(Base):
    __tablename__ = 'node'

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey(Project.id), nullable=False)
    node_type = Column(String(100), nullable=False)
    _input_shape = Column(
        'input_shape', String(1000), default='[]', nullable=False
    )
    _output_shape = Column(
        'output_shape', String(1000), default='[]', nullable=False
    )
    _in_edges = Column('in_edges', String(1000), default='[]', nullable=False)
    _out_edges = Column('out_edge', String(1000), default='[]', nullable=False)
    status = Column(Integer, default=0, nullable=False)  # 0 未运行 1 正在运行 2 运行完成
    _extra = Column('extra', String(1000), default='{}', nullable=False)

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
        return './file/{}/node/{}'.format(self.project_id, self.id)

    def join_path(self, filename):
        return os.path.join(self.dictionary_path, filename)

    @property
    def log(self):
        if os.path.exists(self.join_path('log.txt')):
            with open(self.join_path('log.txt')) as f:
                return f.read()

    def modify(self, **kwargs):
        super().modify(status=0, **kwargs)

    def delete(self):
        nodes = Node.search(project_id=self.project_id, page_size=-1)['data']
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
