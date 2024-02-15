import uuid
from datetime import datetime

from pydantic import BaseModel


class SUser(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    hashed_password: str
    created_at: datetime
    is_active: bool
    is_verified: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class SUserEdit(BaseModel):
    name: str = None
    email: str = None
    is_active: bool = None
    is_verified: bool = None
    is_superuser: bool = None


class SUserDeleteResponse(BaseModel):
    message: str
    user_id: str


class SUserEditResponse(SUserDeleteResponse):
    detail: dict