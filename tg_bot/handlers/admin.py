from aiogram import types, Dispatcher

from tg_bot.config import load_config
from tg_bot.misc.throttling import rate_limit
from tg_bot.misc.twitter import TweetStream

config = load_config('.env')

@rate_limit(5, key='start')
async def admin_start(message: types.Message):
    await message.answer(text='Hello admin!')


@rate_limit(20, key='bot_start')
async def bot_start(message: types.Message):
    global tweet_stream
    tweet_stream = TweetStream(
        consumer_key=config.tw_bot.consumer_key,
        consumer_secret=config.tw_bot.consumer_secret,
        access_token=config.tw_bot.access_token,
        access_token_secret=config.tw_bot.access_secret
    )
    tweet_stream.filter(follow=[config.tw_bot.twitter_id])


@rate_limit(20, key='bot_start')
async def bot_stop(message: types.Message):
    tweet_stream.disconnect()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=['start'], is_admin=True)
    dp.register_message_handler(bot_start, commands=['start_bot'], is_admin=True)
    dp.register_message_handler(bot_stop, commands=['stop_bot'], is_admin=True)
