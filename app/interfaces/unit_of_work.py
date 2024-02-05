from abc import ABC, abstractmethod
from types import TracebackType

from app.users.repository import UsersRepository


class IUnitOfWork(ABC):
    users_repository: UsersRepository

    @abstractmethod
    async def __aenter__(self) -> "IUnitOfWork":
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type: BaseException | None, exc_val: BaseException | None,
                        exc_tb: TracebackType | None) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
