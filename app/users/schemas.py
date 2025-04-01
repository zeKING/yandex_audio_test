import datetime
from typing import List, Optional

from fastapi import UploadFile
from pydantic import BaseModel

from app.repository.schemas import SBaseListResponse


# class SUUser(BaseModel):
#     lastname: str | None
#     name: str | None



class SCurrentUser(BaseModel):
    id: str
    email: str
    login: str

    avatar_id: str | None
    avatar: str | None
    first_name: str | None
    last_name: str | None
    gender: str | None
    phone: str | None

    last_login: datetime.date | None
    created_at: datetime.datetime
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class SUser(BaseModel):
    id: str
    email: str
    avatar: Optional[str]
    avatar_id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    last_login: datetime.date | None
    created_at: datetime.datetime

class SUserList(SBaseListResponse):
    data: List[SUser]


class SUpdateCurrentUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    gender: Optional[str]


class SUserToken(BaseModel):
    access_token: str


class SLogin(BaseModel):
    auth_url: str

