import json

from flask_login import current_user
from sqlalchemy import Column, ForeignKey, Integer, String

from app.libs.helper import get_random_string
from app.models.base import Base
from app.models.user import User


class UserNode(Base):
    __tablename__ = "user_node"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    code = Column(String(100), nullable=False, index=True)
    node_type = Column(String(100), nullable=False)
    _extra = Column("extra", String(1000), default="{}", nullable=False)

    @property
    def extra(self):
        return json.loads(self._extra)

    @extra.setter
    def extra(self, raw):
        self._extra = json.dumps(raw)

    @classmethod
    def get_user_node_by_code(cls, code):
        return cls.query.filter_by(code=code).first()

    @classmethod
    def create(cls, **kwargs):
        code = get_random_string(32)
        return super().create(code=code, user_id=current_user.id, **kwargs)

    def modify(self, **kwargs):
        if kwargs["reset_code"]:
            kwargs["code"] = get_random_string(32)
        super().modify(**kwargs)
