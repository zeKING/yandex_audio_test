import asyncio
import os

from app.config import settings
from app.users.models import User


async def main():

    await User.get_or_create(filter=User.id == settings.SUPERUSER_ID,
                             id=settings.SUPERUSER_ID,
                             email=settings.SUPERUSER_EMAIL,
                             is_superuser=True
                             )

    os.makedirs('media', exist_ok=True)
    # Остальные данные не стал добавлять, чтоб не заморачивались при тестировании

if __name__ == "__main__":
    asyncio.run(main())
