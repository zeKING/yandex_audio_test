import datetime
from typing import List, Optional

from fastapi import UploadFile
from pydantic import BaseModel




# class SUUser(BaseModel):
#     lastname: str | None
#     name: str | None



class SCurrentUser(BaseModel):
    id: int
    email: str
    avatar_id: str | None
    avatar: str | None
    first_name: str | None
    last_name: str | None
    phone: str | None
    last_login: datetime.datetime | None
    created_at: datetime.datetime
    is_active: bool


    class Config:
        from_attributes = True



class SUser(BaseModel):
    id: int
    email: str
    avatar: Optional[str]
    avatar_id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    patronymic: Optional[str]


class SUserToken(BaseModel):
    access_token: str


class SLogin(BaseModel):
    auth_url: str

