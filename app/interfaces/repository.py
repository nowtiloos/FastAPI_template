from abc import ABC, abstractmethod


class IRepository(ABC):
    @abstractmethod
    async def find_all(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def find_by_filter(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def find_one_or_none(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def add(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs):
        raise NotImplementedError


class IUsersRepository(IRepository, ABC):
    ...
