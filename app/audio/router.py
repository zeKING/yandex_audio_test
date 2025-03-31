from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy import and_
from starlette.responses import Response

from app.audio.models import Audio
from app.audio.schemas import SAudioResponse, SAudioListResponse
from app.audio.services import AudioService
from app.repository.tools import get_list_data
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(prefix='/audio', tags=['Аудио'])


@router.post('', response_model=SAudioResponse)
async def create_audio(filename: str = Form(None), file: UploadFile = File(), user: User = Depends(get_current_user)):

    return await AudioService.create_audio(filename, file, user)


@router.get('', response_model=SAudioListResponse)
async def get_audio_list(page: int = 1, limit: int = 10, user: User = Depends(get_current_user)):
    return await get_list_data(Audio, page, limit, filter=Audio.user_id == user.id)


@router.patch('/{audio_id}', response_model=SAudioResponse)
async def update_audio(audio_id: int, filename: str = Form(), user: User = Depends(get_current_user)):
    audio = await Audio.update_by_filter(filter=and_(Audio.id == audio_id, Audio.user_id == user.id),
                                         filename=filename)
    return audio

@router.delete('/{audio_id}', responses={204: {}})
async def delete_audio(audio_id: int, response: Response, user: User = Depends(get_current_user)):
    await AudioService.delete_audio(audio_id, user)

    response.status_code = 204
    return response


