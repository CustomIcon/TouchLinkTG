from pyrogram import Client
from configparser import ConfigParser
import os
from tinydb import TinyDB
import pyromod.listen  # noqa

database = TinyDB('touchlink.json')

config = ConfigParser()
config.read('config.ini')
app = Client(
    name="touchlink",
    api_id=config.getint('pyrogram', 'api_id'),
    api_hash=config.get('pyrogram', 'api_hash'),
    bot_token=config.get('pyrogram', 'bot_token'),
    plugins={'root': os.path.join(__package__, 'plugins')}
)
