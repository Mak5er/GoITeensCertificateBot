import os

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

load_dotenv()

TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    raise Exception("Could not load you bot token, please check your .env file")

bot = AsyncTeleBot(
    token=TOKEN,
    state_storage=StateMemoryStorage()
)
