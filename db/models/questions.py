import datetime

from sqlalchemy import Column, String, BigInteger, Boolean, ForeignKey, DateTime

from db import Base

class Questions(Base):
    __tablename__ = 'questions'

    id = Column(BigInteger, primary_key=True)
    creator_id = Column(BigInteger, ForeignKey('users.id'))
    title = Column(String(50), nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())

class QuestionTypes(Base):
    __tablename__ = 'question_types'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(20), nullable=False)

class Question_settings(Base):
    __tablename__ = 'question_settings'

    question_id = Column(BigInteger, ForeignKey('questions.id'), primary_key=True)
    type_id = Column(BigInteger, ForeignKey('question_types.id'))
    expires_at = Column(DateTime, default= lambda: datetime.datetime.now() + datetime.timedelta(weeks=1)) # конец через 1 неделю
    is_anonymous = Column(Boolean, default=False, nullable=False)
    is_closed = Column(Boolean, default=False, nullable=False)