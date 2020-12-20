import logging
import os
from abc import abstractmethod


class BaseNode:
    def __init__(self, id_, project_id, node_type, in_edges, out_edges):
        self.id = id_
        self.project_id = project_id
        self.node_type = node_type
        self.in_edges = in_edges
        self.out_edges = out_edges
        # shape
        self.input_shape = None
        self.output_shape = None
        # logger
        self.logger = logging.getLogger('node-{}'.format(id_))
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.addHandler(
            logging.FileHandler(self.join_path('log.txt'), mode='w')
        )

    @property
    def dictionary_path(self):
        return './file/{}/node/{}'.format(self.project_id, self.id)

    def join_path(self, filename):
        return os.path.join(self.dictionary_path, filename)

    @abstractmethod
    def run(self):
        pass
