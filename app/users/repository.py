from app.interfaces.repository import IUsersRepository
from app.users.models import User
from app.repositories.base_repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository, IUsersRepository):
    model = User

