from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.dependencies.services import get_users_services
from app.users.models import User
from app.users.schemas import SUser, SUserEdit, SUserEditResponse, SUserDeleteResponse
from app.users.services import UsersServices

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def get_me(user: User = Depends(get_current_user),
           users_services: UsersServices = Depends(get_users_services)
           ) -> SUser:
    return users_services.read_users_me(user)


@router.get("/all")
async def get_all_users(users_services: UsersServices = Depends(get_users_services)
                        ) -> list[SUser]:
    return await users_services.get_all_users()


@router.get("/{id}")
async def get_user_by_id(user_id: str,
                         users_services: UsersServices = Depends(get_users_services)
                         ) -> SUser | None:
    return await users_services.get_user(user_id=user_id)


@router.patch("/{id}/edit")
async def edit_user(user_id: str,
                    data: Annotated[SUserEdit, Depends()],
                    users_services: UsersServices = Depends(get_users_services)
                    ) -> SUserEditResponse:
    return await users_services.edit_user(user_id, data)


@router.delete("{id}")
async def delete_user(user_id: str,
                      users_services: UsersServices = Depends(get_users_services)
                      ) -> SUserDeleteResponse:
    return await users_services.delete_user(user_id)
