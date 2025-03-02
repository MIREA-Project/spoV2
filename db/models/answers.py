import datetime

from sqlalchemy import Column, String, BigInteger, Boolean, ForeignKey, DateTime, Integer, DECIMAL

from db import Base

class UserAnswers(Base):
    __tablename__ = 'user_answers'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    question_id = Column(BigInteger, ForeignKey('questions.id', ondelete='CASCADE'))
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=datetime.datetime.now)
    score_awarded = Column(Integer, nullable=True)

class VotingRatings(Base):
    __tablename__ = 'voting_ratings'

    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    question_id = Column(BigInteger, ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)
    rating = Column(DECIMAL(precision=3, scale=2), nullable=True)

class VotingAnswers(Base):
    __tablename__ = 'voting_answers'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    question_id = Column(BigInteger, ForeignKey('questions.id', ondelete='CASCADE'))
    title = Column(String(20), nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)