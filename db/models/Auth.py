import datetime

from sqlalchemy import Column, String, BigInteger, DateTime, Integer

from db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    nickname = Column(String(20), nullable=False)
    password = Column(String)
    email = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    correct_vote_count = Column(Integer, default=0)
    score = Column(Integer, default=0)
