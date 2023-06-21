import asyncio
import logging

import uvloop
from telebot.async_telebot import asyncio_filters, logger, types

from certificates_bot.bot import bot
from certificates_bot.handlers.create import \
    register_handlers as register_create_handlers


@bot.message_handler(commands=["start"])
async def start(message: types.Message) -> None:
    await bot.send_message(
        message.chat.id,
        text="Привіт, любителю фальшивих паперів. Введи команду /create, щоб створити сертифікат GoITeens, розбійнику",
    )


@bot.message_handler(state="*", commands='cancel')
async def any_state(message):
    await bot.send_message(message.chat.id, "Відмінено")
    await bot.delete_state(message.from_user.id, message.chat.id)




def setup_logger() -> None:
    logger.setLevel(logging.INFO)


async def main() -> None:
    setup_logger()

    register_create_handlers(bot)
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    await bot.polling(non_stop=True)

if __name__ == '__main__':
    with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
        runner.run(main())
