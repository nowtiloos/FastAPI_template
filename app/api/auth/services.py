from datetime import datetime, timedelta
from fastapi import Response

from app.api.auth.schemas import SUserRegister, SUserLogin
from app.config import settings
from app.exceptions.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException, \
    CannotAddDataToDatabase
from app.interfaces.unit_of_work import IUnitOfWork
from passlib.context import CryptContext
from jose import jwt
from pydantic import EmailStr

pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")


class AuthServices:
    def __init__(self, unit_of_work: IUnitOfWork) -> None:
        self.unit_of_work = unit_of_work

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(claims=to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_tokens(data: dict) -> tuple:
        # Создаем access token
        access_token_data = data.copy()
        access_token_expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token_data.update({"exp": access_token_expire})
        access_token = jwt.encode(access_token_data, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        # Создаем refresh token
        refresh_token_data = data.copy()
        refresh_token_expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token_data.update({"exp": refresh_token_expire})
        refresh_token = jwt.encode(refresh_token_data, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        return access_token, refresh_token

    async def authenticate_user(self, email: EmailStr, password: str):
        async with self.unit_of_work as uow:
            user = await uow.users_repository.find_one_or_none(email=email)
            if not (user and self.verify_password(password, user.hashed_password)):
                raise IncorrectEmailOrPasswordException
            return user

    async def register_user(self, user_data: SUserRegister):
        async with self.unit_of_work as uow:
            existing_user = await uow.users_repository.find_one_or_none(email=user_data.email)
            if existing_user:
                raise UserAlreadyExistsException

            hashed_password = self.get_password_hash(user_data.password)
            user_data = user_data.model_dump()
            user_data.pop("password")
            user_data.update({"hashed_password": hashed_password})

            new_user = await uow.users_repository.add(**user_data)
            if not new_user:
                raise CannotAddDataToDatabase
            return {"message": "Регистрация успешно завершена"}

    async def login_user(self, response: Response, user_data: SUserLogin):
        user = await self.authenticate_user(user_data.email, user_data.password)
        # create tokens
        access_token, refresh_token = self.create_tokens({"sub": str(user.id)})
        # set access token to cookie
        response.set_cookie(settings.TOKEN_NAME, access_token, httponly=True)
        # set refresh token to db
        async with self.unit_of_work as uow:
            await uow.users_repository.edit_one(id=user.id, data={"refresh_token": refresh_token})

        return {"message": "Успешный вход в систему", "access_token": access_token, "refresh_token": refresh_token}

    @staticmethod
    async def logout_user(response: Response):
        response.delete_cookie(settings.TOKEN_NAME)
        return {"message": "Успешный выход из системы"}
