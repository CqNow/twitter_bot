from aiogram import Dispatcher

from tg_bot.config import load_config
from tg_bot.misc.discord import send_all
from tweepy.asynchronous import AsyncStream


config = load_config('.env')

class TweetStream(AsyncStream):


    async def on_connect(self):
        dp = Dispatcher.get_current()
        bot = dp.bot
        await bot.send_message(chat_id=config.tg_bot.admin_id, text='Start bot')

    async def on_status(self, status):
        if from_creator(status):
            tweet_text = form_tweet_text(status)
        await send_all(tweet_id=status.id_str, origin_text=tweet_text)

    async def on_disconnect(self):
        dp = Dispatcher.get_current()
        bot = dp.bot
        await bot.send_message(chat_id=config.tg_bot.admin_id, text='Stop Bot')

def from_creator(status):
    """Compare a status id with a user id to check
     if the tweet was sent by the user"""
    if hasattr(status, "retweeted_status"):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True

def form_tweet_text(status):
    """Check for extended_text"""
    if hasattr(status, 'extended_tweet'):
        return status.extended_tweet['full_text']
    else:
        return status.text

