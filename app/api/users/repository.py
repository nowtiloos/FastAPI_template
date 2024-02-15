from app.interfaces.repository import IUsersRepository
from app.api.users.models import User
from app.repositories.base_repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository, IUsersRepository):
    model = User

