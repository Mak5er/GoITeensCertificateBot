import io
from pathlib import Path
from time import perf_counter
from barelimg import draw_on

from PIL import Image, ImageDraw, ImageFont
from pyrogram.client import Client
from pyrogram.handlers.disconnect_handler import DisconnectHandler

from certificates_bot.bot import bot
from certificates_bot.logger import get_logger

logger = get_logger(__name__)


async def handle_disconnect(_: Client) -> None:
    IMAGE.close()


bot.add_handler(DisconnectHandler(handle_disconnect))


def generate_certificate(text: str) -> io.BytesIO:
    start = perf_counter()

    buffer = draw_on(text)

    end = perf_counter()

    logger.info(f'Generated in {end - start}s. size Kbytes: {len(buffer) / 1000}')

    return io.BytesIO(buffer)
