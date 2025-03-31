from fastapi import APIRouter, Depends, Form, UploadFile

from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(prefix='/audio', tags=['Аудио'])


