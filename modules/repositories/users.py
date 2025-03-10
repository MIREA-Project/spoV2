from db.models import User
from modules.repositories import SQLAlchemyAbstractRepository


class UsersInfoRepository(SQLAlchemyAbstractRepository):
    model = User