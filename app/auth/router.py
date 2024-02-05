from fastapi import APIRouter, Depends, Response

from app.auth.schemas import SUserRegister, SRegisterResponse, SUserLogin, SLoginResponse, SLogoutResponse
from app.auth.services import AuthServices
from app.dependencies.services import get_auth_services

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=201)
async def register_user(user_data: SUserRegister,
                        auth_services: AuthServices = Depends(get_auth_services)
                        ) -> SRegisterResponse:
    return await auth_services.register_user(user_data)


@router.post("/login")
async def login_user(response: Response, user_data: SUserLogin,
                     auth_services: AuthServices = Depends(get_auth_services)
                     ) -> SLoginResponse:
    return await auth_services.login_user(response, user_data)


@router.post("/logout")
async def logout_user(response: Response,
                      auth_services: AuthServices = Depends(get_auth_services)
                      ) -> SLogoutResponse:
    return await auth_services.logout_user(response)
