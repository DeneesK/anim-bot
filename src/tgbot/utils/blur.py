import random

from PIL import Image, ImageFilter
from src.tgbot.utils.download import download


async def blur_it(path: str, name: int) -> str:
    # Open existing image

    path = await download(path, name)

    OriImage = Image.open(path)

    # Applying GaussianBlur filter
    gaussImage = OriImage.filter(ImageFilter.GaussianBlur(60))

    out_path, _ = path.split('.')
    out_path = out_path + str(random.randint(0, 500000)) + '.jpg'

    # Save Gaussian Blur Image
    gaussImage.save(out_path)
    return out_path
