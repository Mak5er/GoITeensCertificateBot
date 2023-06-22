import io
from pathlib import Path
from time import perf_counter
from barelimg import draw_on

from pyrogram.client import Client
from pyrogram.handlers.disconnect_handler import DisconnectHandler

from certificates_bot.bot import bot
from certificates_bot.logger import get_logger

logger = get_logger(__name__)


def generate_certificate(text: str) -> io.BytesIO:
    start = perf_counter()

    buffer = draw_on(text)

    end = perf_counter()

    logger.info(f'Generated in {end - start}s. size Kbytes: {len(buffer) / 1000}')

    return io.BytesIO(buffer)
