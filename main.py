import os
import telebot
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

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
    with Image.open("template.png") as im:
        draw = ImageDraw.Draw(im)
        font_path = "Cleanvertising_Black.ttf"
        font_size = 35
        font = ImageFont.truetype(font_path, font_size)
        text_wight = draw.textsize(text=message.text, font=font)
        image_wight = im.size
        text_position = [(image_wight[0] - text_wight[0]) // 2, 620]
        draw.text(text_position, message.text, font=font)
    bot.send_photo(message.chat.id, photo=im)


bot.polling()
