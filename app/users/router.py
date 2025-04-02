from datetime import datetime, timedelta, timezone

from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.config import settings
from app.repository.tools import get_list_data
from app.users.exceptions import TokenAbsentException
from app.users.auth_service import AuthService
from app.users.dependencies import get_current_user, is_admin
from app.users.models import User
from app.users.schemas import SLogin, SUserToken, SCurrentUser, SUpdateCurrentUser, SUserList
from fastapi import APIRouter, Response, Depends, UploadFile, File

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


@router.get("/verify-code", response_model=SUserToken)
async def verify_code(code: str):

    yandex_access_token = await YandexAuthService.get_yandex_access_token(code)
    user_data = await YandexAuthService.get_user_data(yandex_access_token)
    user = await UserService.save_user_data(user_data)
    access_token = AuthService.create_access_token({'sub': str(user.id)})
    refresh_token = AuthService.create_refresh_token({'sub': str(user.id)})

    await User.update(record_id=user.id, last_login=datetime.utcnow())

    response = RedirectResponse(url=settings.FRONTEND_REDIRECT_URI, status_code=302)

    response.set_cookie('access_token', access_token,
                        expires=datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    response.set_cookie('refresh_token', refresh_token,
                        expires=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
                        httponly=True, secure=True)

    # return {"access_token": access_token}

    return response


@router.post("/refresh-token", response_model=SUserToken)
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
    response.delete_cookie("refresh_token")
    return {"detail": "success"}


@router.get("/current-user", response_model=SCurrentUser)
async def current_user(user: User = Depends(get_current_user)):
    print(user.id)
    return user


@router.get("/user/list", response_model=SUserList)
@is_admin()
async def get_users_list(page: int = 1, limit: int = 10, user: User = Depends(get_current_user)):
    return await get_list_data(User, page, limit)


@router.delete("/user/{user_id}", responses={204: {}})
@is_admin()
async def delete_user(user_id: str, user: User = Depends(get_current_user)):
    await UserService.delete_user(user_to_delete_id=user_id, user=user)


@router.put('/current-user', response_model=SCurrentUser)
async def update_current_user(data: SUpdateCurrentUser, user: User = Depends(get_current_user)):

    return await UserService.update_current_user(user=user, data=data.dict())


@router.put('/current-user/avatar')
async def update_current_user_avatar(avatar: UploadFile = File(), user: User = Depends(get_current_user)):
    return await UserService.update_current_user_avatar(user=user, avatar=avatar)
