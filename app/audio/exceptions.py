from fastapi import HTTPException
from starlette import status

InvalidAudioFileExtensionException = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="Неверное расширение файла. Расширение должно быть .wav, .mp3, .ogg"
)