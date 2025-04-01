import base64
import os
import shutil
from secrets import token_hex

from sqlalchemy import and_

from app.config import settings
from app.users.exceptions import YandexAPIError, CantDeleteSelfException
from app.request import request
from app.users.models import User
from app.users.validators import validate_avatar_file
from app.utils import convert_image_to_webp


class YandexAuthService:

    @staticmethod
    async def get_yandex_access_token(code) -> str:
        base64_key = (base64.b64encode(
            f"{settings.YANDEX_CLIENT_ID}:{settings.YANDEX_CLIENT_SECRET}".encode())
                      .decode())
        headers = {
            'Authorization': f"Basic {base64_key}"
        }

        response = await request.post('https://oauth.yandex.ru/token',
                                      headers=headers,
                                      data={'grant_type': 'authorization_code', 'code': code})
        if response['status'] != 200:
            raise YandexAPIError
        return response['body']['access_token']

    @staticmethod
    async def get_user_data(yandex_access_token) -> dict:
        print(yandex_access_token)
        headers = {
            'Authorization': f"OAuth {yandex_access_token}"
        }
        response = await request.get('https://login.yandex.ru/info', headers=headers)

        if response['status'] != 200:
            raise YandexAPIError

        return response['body']


class UserService:
    AVATAR_MEDIA_FOLDER = 'media/users/avatars'
    @staticmethod
    async def save_user_data(user_data):

        user = await User.find_one_or_none(filter=User.id == user_data['id'])
        if user is None:
            phone = user_data.get('default_phone', None)

            if phone is not None:
                phone = phone.get('number')

            data = {
                'id': user_data.get('id'),
                'login': user_data.get('login', None),
                'email': user_data.get('default_email', None),
                'first_name': user_data.get('first_name', None),
                'last_name': user_data.get('last_name', None),
                'gender': user_data.get('sex', None),
                'phone': phone,
                'avatar_id': user_data.get('default_avatar_id', None)

            }
            user = await User.create(**data)

        return user

    @staticmethod
    async def delete_user(user_to_delete_id, user):

        if user_to_delete_id == user.id:
            raise CantDeleteSelfException
        user = await User.find_one_or_fail(filter=User.id == user_to_delete_id)

        avatar = user.avatar

        if avatar:
            os.remove(avatar)

        await User.delete(User.id == user_id)

    @staticmethod
    async def update_current_user(user, data):
        return await User.update(record_id=user.id, **data)

    @staticmethod
    async def update_current_user_avatar(user, avatar):
        user = await User.find_one_or_fail(filter=User.id == user.id)

        old_avatar = user.avatar

        if old_avatar:
            os.remove(old_avatar)

        validate_avatar_file(avatar)

        path = f"{UserService.AVATAR_MEDIA_FOLDER}/{token_hex(16)}.webp"

        os.makedirs(UserService.AVATAR_MEDIA_FOLDER, exist_ok=True)

        webp_image = await convert_image_to_webp(avatar.file)

        with open(path, 'wb') as file_writer:

            shutil.copyfileobj(webp_image, file_writer)

        return await User.update(record_id=user.id, avatar=path)





