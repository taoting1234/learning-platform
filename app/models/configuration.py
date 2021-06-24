from sqlalchemy import Column, Integer, String, Text

from app.models.base import Base


class Configuration(Base):
    __tablename__ = "configuration"

    key = Column(String(100), primary_key=True, nullable=False)
    value = Column(Text, nullable=False)
