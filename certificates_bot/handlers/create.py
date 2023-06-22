import enum
from concurrent.futures.thread import ThreadPoolExecutor
from time import perf_counter

from pyrogram import filters, types
from pyrogram.client import Client
from pyrogram.enums import ChatAction
from pyrogram.handlers.message_handler import MessageHandler
from transitions import Machine

from certificates_bot.fsm import InMemoryStorage, StorageKey
from certificates_bot.logger import get_logger
from certificates_bot.messages import messages
from certificates_bot.utils.generate_certificate import generate_certificate

pool = ThreadPoolExecutor(50)
storage = InMemoryStorage()
logger = get_logger(__name__)


class CreateStates(enum.Enum):
    NAME = 1


async def create_handler(_: Client, message: types.Message):
    await message.reply(
        text=messages.enter_name
    )

    storage.add_entry(
        StorageKey(
            chat_id=message.chat.id,
            user_id=message.from_user.id
        ),
        state_machine=Machine()
    )


async def send_sert_handler(bot: Client, message: types.Message):
    storage_key = StorageKey(
        chat_id=message.chat.id,
        user_id=message.from_user.id
    )

    storage_entry = storage.get_entry(storage_key)

    if storage_entry is None or storage_entry.state.state is CreateStates.NAME:
        return


    if message.text is None:
        await message.reply(
            text=messages.please_sent_text
        )

        return


    await bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
    logger.info(f'Generating certificate for {message.chat.id = }')
    certificate_image = pool.submit(generate_certificate, message.text).result()

    start = perf_counter()
    await bot.send_photo(
        message.chat.id,
        photo=certificate_image,
        reply_to_message_id=message.id,
        caption=messages.certificate_ready
    )

    end = perf_counter()

    logger.info(f'Sent image to {message.chat.id = } in {end - start}s.')
    await bot.send_chat_action(message.chat.id, ChatAction.CANCEL)
    storage.clear_entry(storage_key)


def register_handlers(bot: Client) -> None:
    bot.add_handler(MessageHandler(create_handler, filters.command('create')))
    bot.add_handler(MessageHandler(send_sert_handler))
