import io

from PIL import Image


async def convert_image_to_webp(file):
    image = Image.open(file)
    webp_image_io = io.BytesIO()
    image.save(webp_image_io, format="webp")
    webp_image_io.seek(0)
    return webp_image_io
