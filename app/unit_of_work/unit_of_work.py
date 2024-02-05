from types import TracebackType

from app.database import async_session_maker
from app.interfaces.unit_of_work import IUnitOfWork

from app.users.repository import UsersRepository


class SQLAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self) -> None:
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users_repository = UsersRepository(self.session)

        return self

    async def __aexit__(self, exc_type: BaseException | None, exc_val: BaseException | None,
                        exc_tb: TracebackType | None) -> bool:
        if exc_type:
            await self.rollback()
        else:
            await self.session.commit()
        await self.session.close()
        return False

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
