import strawberry
from strawberry.fastapi import GraphQLRouter

from modules.graphql.context import get_context
from .queries import QuestionsQuery, UserInfoQuery, AnswersQuery
from .mutations import QuestionsMutation, UsersMutation, AnswersMutation


# add graphql router
@strawberry.type
class Query(QuestionsQuery, UserInfoQuery, AnswersQuery):
    pass


@strawberry.type
class Mutation(QuestionsMutation, UsersMutation, AnswersMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context)
