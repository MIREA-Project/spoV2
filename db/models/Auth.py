from sqlalchemy import Column, String, Integer, CheckConstraint, BigInteger, String, Boolean, ForeignKey, TIMESTAMP

from db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
