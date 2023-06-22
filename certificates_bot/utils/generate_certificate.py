import io
from time import perf_counter

from barelimg import draw_on
from certificates_bot.logger import get_logger

logger = get_logger(__name__)


def generate_certificate(text: str) -> io.BytesIO:
    start = perf_counter()

    buffer = draw_on(text)

    end = perf_counter()

    logger.info(f'Generated in {end - start}s. size Kbytes: {len(buffer) / 1000}')

    return io.BytesIO(buffer)
