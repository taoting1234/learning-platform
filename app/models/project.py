import os
import shutil

from flask import current_app
from sqlalchemy import Column, ForeignKey, Integer, String

from app.models.base import Base
from app.models.user import User


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(1000))
    tag = Column(String(100))

    @classmethod
    def create(cls, **kwargs):
        base = super().create(**kwargs)
        os.makedirs(
            '{}/{}'.format(current_app.config['FILE_DIRECTORY'], base.id),
            exist_ok=True
        )
        os.makedirs(
            '{}/{}/user'.format(current_app.config['FILE_DIRECTORY'], base.id),
            exist_ok=True
        )
        os.makedirs(
            '{}/{}/node'.format(current_app.config['FILE_DIRECTORY'], base.id),
            exist_ok=True
        )
        return base

    def delete(self):
        from app.models.file import File
        from app.models.node import Node
        files = File.search(project_id=self.id, page_size=-1)['data']
        for file in files:
            file.delete()
        nodes = Node.search(project_id=self.id, page_size=-1)['data']
        for node in nodes:
            node.delete()
        shutil.rmtree(
            '{}/{}'.format(current_app.config['FILE_DIRECTORY'], self.id)
        )
        super().delete()

    def run(self):
        from app.models.node import Node
        nodes = Node.search(project_id=self.id, page_size=-1)['data']
        run_node = None
        for node in nodes:
            if not node.out_edges:
                if run_node is None:
                    run_node = node
                else:
                    assert False, 'Project has multiple graph'
        assert run_node, 'Graph have cycle'
        run_node.run()
