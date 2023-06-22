import io
from pathlib import Path
from time import perf_counter

from PIL import Image, ImageDraw, ImageFont
from pyrogram.client import Client
from pyrogram.handlers.disconnect_handler import DisconnectHandler

from certificates_bot.bot import bot
from certificates_bot.logger import get_logger

logger = get_logger(__name__)

STATIC_DIR = Path("./static")
TEMPLATE_IMAGE = STATIC_DIR.joinpath(Path("./template.png"))
FONT_IMAGE = 35
FONT = ImageFont.truetype(
    str(STATIC_DIR.joinpath(Path("./Cleanvertising_Black.ttf")).absolute()),
    FONT_IMAGE
)

IMAGE = Image.open(TEMPLATE_IMAGE)


async def handle_disconnect(_: Client) -> None:
    IMAGE.close()


bot.add_handler(DisconnectHandler(handle_disconnect))


def generate_certificate(text: str) -> io.BytesIO:
    start = perf_counter()

    image = IMAGE.copy()
    draw = ImageDraw.Draw(image)
    text_wight = draw.textsize(text=text, font=FONT)
    image_wight = image.size
    text_position = (image_wight[0] - text_wight[0]) // 2, 620
    draw.text(text_position, text, font=FONT)
    
    buffer = io.BytesIO()
    image.save(buffer, 'png')
    end = perf_counter()

    image_size = buffer.getbuffer().nbytes
    logger.info(f'Generated in {end - start}s. size Kbytes: {image_size / 1000}')

    return buffer
