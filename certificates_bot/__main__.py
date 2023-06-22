from pyrogram import filters, types
from pyrogram.client import Client

from certificates_bot.bot import bot
from certificates_bot.handlers.create import \
    register_handlers as register_create_handlers
from certificates_bot.logger import setup_loggers


@bot.on_message(filters.command(['start']))
async def start_handler(_: Client, message: types.Message):
    await message.reply(
        text="Привіт, любителю фальшивих паперів. Введи команду /create, щоб створити сертифікат GoITeens, розбійнику",
    )


def main() -> None:
    setup_loggers()

    register_create_handlers(bot)

    bot.run()

if __name__ == '__main__':
    main()
