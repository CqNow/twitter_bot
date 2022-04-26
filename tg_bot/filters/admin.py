from aiogram.dispatcher.filters import BoundFilter

from tg_bot.config import Config


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin=None):
        self.is_admin = is_admin

    async def check(self, obj):
        if self.is_admin is None:
            return
        config: Config = obj.bot.get('config')
        user_id = obj.from_user.id
        return str(user_id) == config.tg_bot.admin_id
