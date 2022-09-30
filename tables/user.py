from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from start.engine import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, )
    email = Column(String(255), nullable=False, unique=True, )
    username = Column(String(255), nullable=False, unique=True, )
    password_hash = Column(String(255))

    created_on = Column(DateTime(), default=datetime.now, )
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now, )
