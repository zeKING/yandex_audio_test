from fastapi import HTTPException
from starlette import status

InvalidFileExtensionException = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid file extension. Extension must be .wav, .mp3, .ogg"
)