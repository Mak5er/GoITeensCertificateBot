import io
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from PIL import Image, ImageDraw, ImageFont
import config

import sqlite3

bot = Bot(token=config.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class CommandState:
    waiting_for_name = "waiting_for_name"


class DataBase:

    def __init__(self, db_file):
        self.connect = sqlite3.connect(db_file)
        self.cursor = self.connect.cursor()

    async def add_users(self, user_id, user_name, user_username):
        with self.connect:
            return self.cursor.execute(
                """INSERT OR IGNORE INTO users (user_id, user_name, user_username) VALUES (?, ?, ?)""",
                (user_id, user_name, user_username))

    async def all_users_count(self):
        with self.connect:
            return self.cursor.execute(
                "SELECT COUNT(*) FROM users").fetchone()[0]

    async def all_users(self):
        with self.connect:
            return self.cursor.execute(
                "SELECT DISTINCT user_id FROM users").fetchall()


db = DataBase('users.db')


@dp.message_handler(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    user_username = message.from_user.username

    await db.add_users(user_id, user_name, user_username)
    await message.answer(
        "Привіт, любителю фальшивих паперів. Введи команду /create, щоб створити сертифікат GoITeens, розбійнику."
    )


@dp.message_handler(Command("create"))
async def create(message: types.Message, state: FSMContext):
    await message.answer("Введіть своє ім'я, щоб згенерувати сертифікат!")

    await state.set_state(CommandState.waiting_for_name)


@dp.message_handler(state=CommandState.waiting_for_name)
async def send_certificate(message: types.Message, state: FSMContext):
    clock = await bot.send_message(message.chat.id, "⏳")
    
    await asyncio.sleep(1)

    with Image.open("template.png") as im:
        draw = ImageDraw.Draw(im)
        font_path = "OpenSans-SemiBold.ttf"
        font_size = 75
        font = ImageFont.truetype(font_path, font_size)
        text_wight = draw.textsize(text=message.text, font=font)
        image_wight = im.size
        text_position = ((image_wight[0] - text_wight[0]) // 2, 1233)
        draw.text(text_position, message.text, font=font)

        image_buffer = io.BytesIO()
        im.save(image_buffer, format="PNG")
        image_buffer.seek(0)

    await asyncio.sleep(1)

    await bot.delete_message(message.chat.id, clock.message_id)
    await message.answer_photo(image_buffer)
    await state.finish()


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    user_id = message.from_user.id
    all_users_count = await db.all_users_count()

    admin_keyboard = InlineKeyboardMarkup()
    send_to_all_button = InlineKeyboardButton(text='💬Mailing',
                                              callback_data='send_to_all')

    admin_keyboard.row(send_to_all_button)

    print(config.ADMIN_ID)

    if user_id == int(config.ADMIN_ID):
        await message.reply(f"""Привіт, це панель адміністратора.
_🪪Кількість користувачів бота_: *{all_users_count}*
""",
                            parse_mode="Markdown",
                            reply_markup=admin_keyboard)

    else:
        await message.reply("Ви не маєте прав адміністратора!")


@dp.callback_query_handler(lambda call: call.data == 'send_to_all')
async def send_to_all_callback(call: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    cancel = types.KeyboardButton("↩️Cancel")
    keyboard.add(cancel)

    await bot.delete_message(call.message.chat.id, call.message.message_id)

    await bot.send_message(chat_id=call.message.chat.id,
                           text='Введіть повіоомення для віправки:',
                           reply_markup=keyboard)
    await dp.current_state().set_state("send_to_all_message")


@dp.message_handler(state="send_to_all_message")
async def send_to_all_message(message: types.Message, state: FSMContext):
    sender_id = message.from_user.id

    if message.text == "↩️Cancel":
        await bot.send_message(message.chat.id,
                               'Розслику скасовано!',
                               reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        await dp.bot.send_chat_action(message.chat.id, "typing")

        users = await db.all_users()

        for user in users:
            try:
                await bot.copy_message(chat_id=user[0],
                                       from_chat_id=sender_id,
                                       message_id=message.message_id,
                                       parse_mode="Markdown")
            except Exception as e:
                print(f"Error sending message to user {user[0]}: {str(e)}")
                continue
        await bot.send_message(chat_id=message.chat.id,
                               text="Sending finished!",
                               reply_markup=ReplyKeyboardRemove())
        await state.finish()


if __name__ == "__main__":
    import keep_alive
    keep_alive.keep_alive()

    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
