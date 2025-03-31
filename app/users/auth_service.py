from datetime import datetime, timedelta

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import settings
from app.users.exceptions import IncorrectTokenException, TokenExpiredException, UserIsNotPresentException
from app.users.models import User

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @staticmethod
    def get_hashed_password(password: str) -> str:
        return password_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_pass: str) -> bool:
        return password_context.verify(password, hashed_pass)

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire, "type": 'access'})
        encoded_jwt = jwt.encode(to_encode, settings.KEY, settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": 'refresh'})
        encoded_jwt = jwt.encode(to_encode, settings.KEY, settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def refresh_access_token(refresh_token: str) -> str:
        try:
            payload = jwt.decode(refresh_token, settings.KEY, settings.ALGORITHM)
        except JWTError:
            raise IncorrectTokenException
        expire: str = payload.get("exp")
        if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
            raise TokenExpiredException
        user_id: str = payload.get("sub")
        if not user_id:
            raise UserIsNotPresentException

        return AuthService.create_access_token({"sub": user_id})

    @staticmethod
    async def authenticate_user(email: str, password: str):
        user = await User.find_one_or_none(User.email == email)

        if not user or not AuthService.verify_password(password, user.hashed_password):
            return None

        return user
