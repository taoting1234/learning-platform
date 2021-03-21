from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.base import Base


class User(UserMixin, Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True)
    organization = Column(String(100), nullable=False, default="无组织")
    _password = Column("password", String(100), nullable=False)
    permission = Column(Integer, nullable=False, default=0)
    block = Column(Integer, nullable=False, default=0)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        if not self._password or not raw:
            return False
        return check_password_hash(self._password, raw)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()
