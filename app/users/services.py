from app.interfaces.unit_of_work import IUnitOfWork
from app.users.schemas import SUserEdit


class UsersServices:
    def __init__(self, unit_of_work: IUnitOfWork):
        self.unit_of_work = unit_of_work

    @staticmethod
    def read_users_me(current_user):
        return current_user

    async def get_all_users(self):
        async with self.unit_of_work as uow:
            return await uow.users_repository.find_all()

    async def get_user(self, user_id: int):
        async with self.unit_of_work as uow:
            return await uow.users_repository.find_one_or_none(id=user_id)

    async def edit_user(self, user_id: int, user: SUserEdit):
        user_dict = user.model_dump(exclude_none=True)
        async with self.unit_of_work as uow:
            await uow.users_repository.edit_one(user_id, user_dict)
            return {"message": "Пользователь изменен", "user_id": user_id, "detail": user_dict}

    async def delete_user(self, user_id: int):
        async with self.unit_of_work as uow:
            await uow.users_repository.delete(id=user_id)
            return {"message": "Пользователь удален", "user_id": user_id}
