import os
import shutil

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
        os.makedirs('./file/{}'.format(base.id), exist_ok=True)
        os.makedirs('./file/{}/user'.format(base.id), exist_ok=True)
        os.makedirs('./file/{}/node'.format(base.id), exist_ok=True)
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
        shutil.rmtree('./file/{}'.format(self.id))
        super().delete()
