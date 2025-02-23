import datetime

from sqlalchemy import Column, String, BigInteger, Boolean, ForeignKey, DateTime, Integer, DECIMAL

from db import Base

class UserAnswers(Base):
    __tablename__ = 'user_answers'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    question_id = Column(BigInteger, ForeignKey('questions.id'))
    user_id = Column(BigInteger, ForeignKey('users.id'))
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())
    score_awarded = Column(Integer, nullable=True)

class VotingRatings(Base):
    __tablename__ = 'voting_ratings'

    user_id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    question_id = Column(BigInteger, ForeignKey('questions.id'), nullable=False)
    rating = Column(DECIMAL(precision=3, scale=2), nullable=True)

class VotingOptions(Base):
    __tablename__ = 'voting_options'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    question_id = Column(BigInteger, ForeignKey('questions.id'))
    title = Column(String(20), nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now())

class NumericAnswers(Base):
    __tablename__ = 'numeric_answers'

    option_id = Column(BigInteger, ForeignKey('voting_options.id'), primary_key=True)
    value = Column(DECIMAL(precision=10, scale=2), nullable=False)

class TextAnswers(Base):
    __tablename__ = 'text_answers'

    option_id = Column(BigInteger, ForeignKey('voting_options.id'), primary_key=True)
    value = Column(String(20), nullable=False)

class BooleanAnswers(Base):
    __tablename__ = 'boolean_answers'

    option_id = Column(BigInteger, ForeignKey('voting_options.id'), primary_key=True)
    value = Column(Boolean, default=False, nullable=False)