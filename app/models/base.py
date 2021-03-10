from contextlib import contextmanager

from flask_sqlalchemy import BaseQuery
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        yield
        self.session.commit()


db = SQLAlchemy(query_class=BaseQuery)


class Base(db.Model):
    __tablename__ = ""
    __abstract__ = True
    __table_args__ = {"extend_existing": True}

    @classmethod
    def get_by_id(cls, id_):
        return cls.query.get(id_)

    @classmethod
    def create(cls, **kwargs):
        base = cls()
        with db.auto_commit():
            for key, value in kwargs.items():
                if value is not None:
                    if hasattr(cls, key):
                        setattr(base, key, value)
            db.session.add(base)
        return base

    def modify(self, **kwargs):
        with db.auto_commit():
            for key, value in kwargs.items():
                if value is not None:
                    if hasattr(self, key):
                        setattr(self, key, value)

    def delete(self):
        with db.auto_commit():
            db.session.delete(self)

    @classmethod
    def search(cls, **kwargs):
        res = cls.query
        for key, value in kwargs.items():
            if value is not None:
                if hasattr(cls, key):
                    if isinstance(value, str):
                        res = res.filter(getattr(cls, key).like(value))
                    else:
                        res = res.filter(getattr(cls, key) == value)

        page = int(kwargs.get("page")) if kwargs.get("page") else 1
        page_size = int(kwargs.get("page_size")) if kwargs.get("page_size") else 20
        data = {"meta": {"count": res.count(), "page": page, "page_size": page_size}}

        if page_size != -1:
            res = res.offset((page - 1) * page_size).limit(page_size)
        res = res.all()
        data["data"] = res
        return data
