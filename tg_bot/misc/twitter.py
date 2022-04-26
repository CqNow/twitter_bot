from aiogram import Dispatcher

from tg_bot.config import load_config
from tg_bot.misc.discord import send_all
from tweepy.asynchronous import AsyncStream

config = load_config('.env')


class TweetStream(AsyncStream):

    test_word = ''

    async def on_connect(self):
        self.test_word = 'Online'
        bot = Dispatcher.get_current().bot
        await bot.send_message(chat_id=config.tg_bot.admin_id, text='Bot has been started')

    async def on_status(self, status):
        if from_creator(status):
            tweet_text = form_tweet_text(status)
        await send_all(tweet_id=status.id_str, origin_text=tweet_text)

    async def on_disconnect(self):
        self.test_word = 'Offline'
        bot = Dispatcher.get_current().bot
        await bot.send_message(chat_id=config.tg_bot.admin_id, text='Bot has been stopped')

    async def on_connection_error(self):
        bot = Dispatcher.get_current().bot
        await bot.send_message(chat_id=config.tg_bot.admin_id, text='Connection Error')

    async def on_exception(self, exception):
        bot = Dispatcher.get_current().bot
        await bot.send_message(chat_id=config.tg_bot.admin_id, text=str(exception))
        await bot.send_message(chat_id=config.tg_bot.admin_id, text='Перезапустите бота')

    async def on_keep_alive(self):
        return self.test_word

    async def on_limit(self, track):
        bot = Dispatcher.get_current().bot
        await bot.send_message(chat_id=config.tg_bot.admin_id, text=str(track))


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
