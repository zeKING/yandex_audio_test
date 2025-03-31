import base64
import os
import shutil
from datetime import datetime, timedelta, timezone

from secrets import token_hex
from typing import List

from starlette.requests import Request

from app.config import settings
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPassword, TokenAbsentException
from app.repository.tools import get_list_data
from app.request import request
from app.users.auth_service import AuthService
from app.users.dependencies import get_current_user
from app.users.models import User
from app.users.schemas import SCurrentUser, SUserToken, SLogin
from fastapi import APIRouter, Response, Depends, UploadFile, Form

from app.users.services import YandexAuthService, UserService

router = APIRouter(prefix="/auth", tags=["Авторизация/Аутентификация"])


@router.post("/login", response_model=SLogin)
async def login():

    auth_url = (f"https://oauth.yandex.ru/authorize"
                f"?response_type=code"
                f"&client_id={settings.YANDEX_CLIENT_ID}"
                f"&redirect_uri={settings.YANDEX_REDIRECT_URI}"
                f"&force_confirm=yes")
    # force_confirm, чтоб каждый раз окно входа выходило

    return {'auth_url': auth_url}

@router.get("/verify-code")
async def verify_code(code: str, response: Response):

    yandex_access_token = await YandexAuthService.get_yandex_access_token(code)
    user_data = await YandexAuthService.get_user_data(yandex_access_token)
    user = await UserService.save_user_data(user_data)
    access_token = AuthService.create_access_token({'sub': str(user.id)})
    refresh_token = AuthService.create_refresh_token({'sub': str(user.id)})

    await User.update(record_id=user.id, last_login=datetime.utcnow())

    response.set_cookie('access_token', access_token,
                        expires=datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    response.set_cookie('refresh_token', refresh_token,
                        expires=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
                        httponly=True, secure=True)

    return {"access_token": access_token}


@router.post("/refresh-token")
async def refresh_access_token(request: Request, response: Response):
    refresh_token = request.cookies.get('refresh_token')
    if refresh_token is None:
        raise TokenAbsentException

    access_token = AuthService.refresh_access_token(refresh_token)
    response.set_cookie('access_token', access_token,
                        expires=datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))



    return {"access_token": access_token}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"detail": "success"}


@router.get("/current-user")
async def current_user(user: User = Depends(get_current_user)):
    return user





