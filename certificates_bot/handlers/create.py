from concurrent.futures.thread import ThreadPoolExecutor

from telebot.async_telebot import AsyncTeleBot, types
from telebot.asyncio_handler_backends import State, StatesGroup

from certificates_bot.bot import bot
from certificates_bot.utils.generate_certificate import generate_certificate

pool = ThreadPoolExecutor(50)


class CreateStates(StatesGroup):
    name = State()


async def create_handler(message: types.Message) -> None:
    await bot.set_state(
        message.from_user.id,
        CreateStates.name,
        message.chat.id
    )

    await bot.send_message(
        message.chat.id, text="Введіть своє ім'я, щоб згенерувати сертифікат"
    )



async def send_sert_handler(message: types.Message):
    if message.text is None:
        await bot.reply_to(
            message,
            text="Будь ласка, надішліть текст, який ви хоче бачити на сертифікаті"
        )

        return

    input_file = pool.submit(generate_certificate, message.text).result()
    await bot.send_photo(message.chat.id, photo=input_file)
    await bot.delete_state(
        message.from_user.id,
        message.chat.id
    )

def register_handlers(bot: AsyncTeleBot) -> None:
    bot.register_message_handler(create_handler, commands=["create"])
    bot.register_message_handler(send_sert_handler, state=CreateStates.name)
