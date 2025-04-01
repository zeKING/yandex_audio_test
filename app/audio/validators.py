from app.audio.exceptions import InvalidAudioFileExtensionException


def validate_audio_file(file):
    file_extension = file.filename.split('.')[-1]
    if file_extension not in ['wav', 'mp3', 'ogg']:
        raise InvalidAudioFileExtensionException

