from typing import Type

from fastapi import Depends

from app.api.auth.services import AuthServices, TokenManager
from app.dependencies.unit_of_work import get_unit_of_work
from app.api.users.services import UsersServices
from app.interfaces.unit_of_work import IUnitOfWork


def get_users_services(unit_of_work: IUnitOfWork = Depends(get_unit_of_work)) -> UsersServices:
    return UsersServices(unit_of_work)


def get_auth_services(unit_of_work: IUnitOfWork = Depends(get_unit_of_work)) -> AuthServices:
    return AuthServices(unit_of_work, token_manager=TokenManager())
