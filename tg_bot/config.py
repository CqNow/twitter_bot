from typing import List
from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_id: str
    use_redis: bool


@dataclass
class TwBot:
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_secret: str
    twitter_id: int
    username: str


@dataclass
class Misc:
    webhook_url: str
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    tw_bot: TwBot
    misc: Misc


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str('BOT_TOKEN'),
            admin_id=env.str('ADMINS'),
            use_redis=env.bool('USER_REDIS')
        ),
        tw_bot=TwBot(
            consumer_key=env.str('CONSUMER_KEY'),
            consumer_secret=env.str('CONSUMER_SECRET'),
            access_token=env.str('ACCESS_TOKEN'),
            access_secret=env.str('ACCESS_SECRET'),
            twitter_id=env.int('TWITTER_ID'),
            username=env.str('TWIITER_NAME')
        ),
        misc=Misc(
            webhook_url=env.str('WEBHOOK_URL')
        )
    )
