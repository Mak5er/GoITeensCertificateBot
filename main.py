import os
import telebot
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
from barelimg import draw_on

load_dotenv()

bot = telebot.TeleBot(token=os.getenv("TOKEN"))


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        text="Привіт, любителю фальшивих паперів. Введи команду /create, щоб створити сертифікат GoITeens, розбійнику",
    )


@bot.message_handler(commands=["create"])
def create(message):
    bot.send_message(
        message.chat.id, text="Введіть своє ім'я, щоб згенерувати сертифікат"
    )
    bot.register_next_step_handler(message, send_sert)


def send_sert(message):
    #with open("template.png", "rb") as im:
    m = draw_on(message.text)  # im.read(), 
    bot.send_photo(message.chat.id, photo=m)


bot.polling()
