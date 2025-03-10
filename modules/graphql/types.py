import strawberry
from typing import Optional
import datetime
from decimal import Decimal


# Типы GraphQL
@strawberry.type
class QuestionsG:
    id: int
    user_id: int
    title: str
    description: Optional[str]
    created_at: datetime.datetime


@strawberry.type
class QuestionTypesG:
    id: int
    name: str


@strawberry.type
class QuestionSettingsG:
    question_id: int
    question_type_id: Optional[int]
    expires_at: Optional[datetime.datetime]
    is_anonymous: bool
    is_closed: bool


@strawberry.type
class UserAnswersG:
    id: int
    question_id: int
    user_id: int
    created_at: datetime.datetime
    score_awarded: Optional[int]


@strawberry.type
class VotingRatingsG:
    user_id: int
    question_id: int
    rating: Optional[Decimal]


@strawberry.type
class VotingAnswersG:
    id: int
    question_id: int
    title: str
    description: Optional[str]
    created_at: datetime.datetime


@strawberry.type
class UserInfoG:
    id: int
    nickname: str
    email: str
    created_at: datetime.datetime
    correct_vote_count: int
    score: int