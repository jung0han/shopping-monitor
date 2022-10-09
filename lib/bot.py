from telegram import Bot
from config import Settings

bot = Bot(Settings().bot_token)


async def echo(text):
    await bot.send_message(chat_id=286215445, text=text)
