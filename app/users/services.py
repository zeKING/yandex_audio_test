import base64

from app.config import settings
from app.exceptions import YandexAPIError
from app.request import request
from app.users.models import User


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

        print(user.id, user.email)
        return user
