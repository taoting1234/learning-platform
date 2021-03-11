from flask_login import current_user
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.libs.helper import get_random_string
from app.models.base import Base
from app.models.user import User


class InvitationCode(Base):
    __tablename__ = "invitation_code"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    is_used = Column(Boolean, nullable=False, default=False)

    @classmethod
    def create(cls, **kwargs):
        code = get_random_string(32)
        return super().create(code=code, user_id=current_user.id, **kwargs)

    @classmethod
    def check_and_use_code(cls, code):
        res = cls.query.filter(cls.code == code, cls.is_used == 0).first()
        if res:
            res.modify(is_used=True)
            return True
        return False
