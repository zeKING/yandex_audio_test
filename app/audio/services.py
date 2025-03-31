import os
import shutil
from secrets import token_hex

from sqlalchemy import and_

from app.audio.models import Audio
from app.audio.validators import validate_audio_file


class AudioService:

    AUDIO_MEDIA_FOLDER = 'media/audio'

    @staticmethod
    async def create_audio(filename, file, user):

        validate_audio_file(file)

        file_extension = file.filename.split('.')[-1]
        path = f"{AudioService.AUDIO_MEDIA_FOLDER}/{token_hex(16)}.{file_extension}"

        os.makedirs(AudioService.AUDIO_MEDIA_FOLDER, exist_ok=True)

        with open(path, 'wb') as file_writer:
            shutil.copyfileobj(file.file, file_writer)

        audio = await Audio.create(filename=filename, file=path, user_id=user.id)

        return audio

    @staticmethod
    async def delete_audio(audio_id, user):

        audio = await Audio.find_one_or_fail(filter=and_(Audio.id == audio_id, Audio.user_id == user.id))

        path = audio.file
        os.remove(path)

        await Audio.delete(filter=Audio.id == audio_id)