import glob
import os
from datetime import datetime

from telebot import types
import logging.config

from telebot.async_telebot import AsyncTeleBot
import asyncio

API_TOKEN = os.environ['TELEGRAM_TOKEN']
bot = AsyncTeleBot(API_TOKEN)
PATH = os.getcwd()
log_file_path = f"{PATH}/app/logger.conf"
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger("TelegramBot")


class TelegramBot:

    # Handle '/start' and '/help'
    @bot.message_handler(commands=['help'])
    async def send_welcome(message):
        await bot.reply_to(message, """\
    Hi there, I am EchoBot.
    I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
    """)

    # Handle '/start' and '/help'
    @bot.message_handler(commands=['looking_for_parking'])
    async def send_welcome(message):
        await bot.send_message(message.chat.id,
                               "This in the future will send you notifications about available parking spots")

    # Handle '/start' and '/help'
    @bot.message_handler(commands=['current_status'])
    async def send_welcome(message):
        date = datetime.now().strftime("%m-%d-%Y")
        hour = datetime.now().strftime("%H:%M:%S")
        #TODO handle list of files is empty cuz of date change 
        logger.info(f"{message.chat.first_name} requested to see status ")
        dir_name = f"app/changes/{date}"
        list_of_files = glob.glob(
            f'/home/eyal/Pycharmprojects/ParkingDetections/{dir_name}/*')  # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        await bot.send_photo(message.chat.id, photo=open(latest_file, "rb"))
        await bot.send_message(message.chat.id,
                               f"{date}-{latest_file.split('/')[-1].split('-')[0]} \n amount of cars :{latest_file.split('/')[-1].split('-')[1]} ")

    # Handle all other messages with content_type 'text' (content_types defaults to ['text'])
    @bot.message_handler(func=lambda m: True)
    async def echo_message(message):
        button1 = types.KeyboardButton(text="/looking_for_parking")
        button2 = types.KeyboardButton(text='/current_status')

        keybord1 = types.ReplyKeyboardMarkup(row_width=2)
        keybord1.add(button1, button2)
        message.text = None
        await bot.send_message(chat_id=message.chat.id, text="Please select one of the options:", reply_markup=keybord1)
        # await bot.reply_to(message," ",reply_markup=keybord1  )

    def __init__(self):
        pass

    @staticmethod
    def run():
        logger.info("Starting Telegram bot...")
        asyncio.run(bot.polling())
