from app.users.exceptions import InvalidAvatarFileExtensionException


def validate_avatar_file(file):
    file_extension = file.filename.split('.')[-1]
    if file_extension not in ['jpg', 'jpeg', 'png', 'jfif', 'webp']:
        raise InvalidAvatarFileExtensionException

