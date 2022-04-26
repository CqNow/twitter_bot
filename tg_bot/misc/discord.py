from dhooks import Webhook, Embed

from tg_bot.config import load_config
from tg_bot.misc.translator import trans

config = load_config('.env')

hook = Webhook(url=config.misc.webhook_url,
               username=config.tw_bot.username,
               avatar_url="https://assets.primagames.com/media/files/true-colors-emblem-destiny-2.jpg"
               )

async def send_all(tweet_id: str, origin_text: str):
    translated_text = trans(origin_text)
    embed = Embed(
        description=translated_text,
        color=0xFF0000,
        timestamp='now'
    )
    embed.set_author(name='Embed Name')
    embed.add_field(name='Field name 1', value='text')
    embed.add_field(name='Field name 2', value='text')
    hook.send(f'https://twitter.com/{config.tw_bot.username}/status/{tweet_id}')
    hook.send(embed=embed)
