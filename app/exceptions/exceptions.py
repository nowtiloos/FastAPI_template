from fastapi import HTTPException, status


class ProjectException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)


class CannotAddDataToDatabase(ProjectException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить запись"


class IncorrectEmailOrPasswordException(ProjectException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class UserAlreadyExistsException(ProjectException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class TokenAbsentException(ProjectException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class TokenExpiredException(ProjectException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class IncorrectTokenFormatException(ProjectException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(ProjectException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токена для этого пользователя не существует"

