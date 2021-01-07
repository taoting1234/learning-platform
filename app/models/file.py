import datetime
import os
import shutil

from flask import current_app
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.models.base import Base
from app.models.project import Project


class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey(Project.id), nullable=False)
    filename = Column(String(100))
    size = Column(Integer)
    access_time = Column(DateTime)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)

    @property
    def path(self):
        return self.join_path(self.filename) if self.filename else None

    def join_path(self, filename):
        return os.path.join(
            "{}/{}/user/".format(current_app.config["FILE_DIRECTORY"], self.project_id),
            filename,
        )

    @classmethod
    def create(cls, **kwargs):
        file = kwargs["file"]
        filename = file.filename.split("/")[-1]
        file_path = os.path.join(kwargs["prefix"], filename)
        file_path = file_path.lstrip("/")
        res = cls.search(project_id=kwargs["project_id"], filename=file_path)["data"]
        if not res:
            base = super().create(**kwargs)
        else:
            base = res[0]
        base.modify(filename=file_path, move_file=False)
        os.makedirs(os.path.split(base.path)[0], exist_ok=True)
        file.save(base.path)
        base.update_meta()
        return base

    def modify(self, **kwargs):
        old_path = self.path
        super().modify(**kwargs)
        if kwargs.get("move_file"):
            dest_path = self.join_path(kwargs["filename"])
            os.makedirs(os.path.split(dest_path)[0], exist_ok=True)
            shutil.move(old_path, dest_path)

    def delete(self):
        super().delete()
        os.remove(self.path)

    def update_meta(self):
        size = os.path.getsize(self.path)
        access_time = datetime.datetime.fromtimestamp(os.path.getatime(self.path))
        create_time = datetime.datetime.fromtimestamp(os.path.getctime(self.path))
        modify_time = datetime.datetime.fromtimestamp(os.path.getmtime(self.path))
        self.modify(
            size=size,
            access_time=access_time,
            create_time=create_time,
            modify_time=modify_time,
            move_file=False,
        )
