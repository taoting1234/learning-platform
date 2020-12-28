import logging
import os

from flask import current_app

from app.models.node import Node


class BaseNode:
    def __init__(self, id_, node_type, project_id, in_edges, out_edges):
        self.id = id_
        self.node_type = node_type
        self.project_id = project_id
        self.in_edges = in_edges
        self.out_edges = out_edges
        # shape
        self.input_shape = []
        self.output_shape = []
        # logger
        self.logger = logging.getLogger('node-{}'.format(id_))
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(filename)s: %(levelname)s %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        file_handler = logging.FileHandler(self.join_path('log.txt'), mode='w')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)

    def dictionary_path(self, id_=None):
        return '{}/{}/node/{}'.format(
            current_app.config['FILE_DIRECTORY'], self.project_id,
            self.id if id_ is None else id_
        )

    def join_path(self, filename, id_=None):
        return os.path.join(self.dictionary_path(id_), filename)

    def update(self):
        node = Node.get_by_id(self.id)
        node.modify(
            input_shape=self.input_shape, output_shape=self.output_shape
        )
