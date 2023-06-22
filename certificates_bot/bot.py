from os import environ
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel
from pyrogram.client import Client


class Config(BaseModel):
    app_hash: str
    bot_token: str
    app_id: int


def load_config() -> Config:
    load_dotenv()
    name_value: dict[str, Any] = dict()

    for name in map(str.upper, Config.__fields__.keys()):
        value = environ.get(name, None)

        if value is None:
            raise Exception(f"Could not load {name}, please check your .env file")

        name_value[name.lower()] = value

    return Config.parse_obj(name_value)


config = load_config()
bot = Client(
    name='my_bot',
    bot_token=config.bot_token,
    api_id=config.app_id,
    api_hash=config.app_hash
)
