import datetime

from sqlalchemy import Column, String, BigInteger, Boolean, ForeignKey, DateTime

from db import Base


class Questions(Base):
    __tablename__ = 'questions'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'))
    title = Column(String(50), nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)


class QuestionTypes(Base):
    __tablename__ = 'question_types'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)


class QuestionSettings(Base):
    __tablename__ = 'question_settings'

    question_id = Column(BigInteger, ForeignKey('questions.id', ondelete='CASCADE'), primary_key=True)
    question_type_id = Column(BigInteger, ForeignKey('question_types.id', ondelete='SET NULL'))
    expires_at = Column(DateTime, nullable=True)
    is_anonymous = Column(Boolean, default=False, nullable=False)
    is_closed = Column(Boolean, default=False, nullable=False)
