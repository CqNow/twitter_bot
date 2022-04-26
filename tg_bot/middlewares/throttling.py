import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import current_handler, CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def throttle(self, target: types.Message | types.CallbackQuery):
        handler = current_handler.get()
        if not handler:
            return

        dp = Dispatcher.get_current()
        limit = getattr(handler, 'throttling_rate_limit', self.limit)
        key = getattr(handler, 'throttling_key', f'{self.prefix}_{handler.__name__}')

        try:
            await dp.throttle(key, rate=limit)
        except Throttled as t:
            await self.target_throttled(target, t, dp, key)
            raise CancelHandler()

    @staticmethod
    async def target_throttled(target: types.Message | types.CallbackQuery,
                               throttled: Throttled, dispatcher: Dispatcher, key: str):
        msg = target.message if isinstance(target, types.CallbackQuery) else target
        delta = throttled.rate - throttled.delta
        bot = Dispatcher.get_current().bot
        if throttled.exceeded_count == 2:
            await bot.send_message(chat_id=msg.from_user.id, text='Слишком часто')
            return
        elif throttled.exceeded_count == 3:
            await bot.send_message(chat_id=msg.from_user.id, text=f'Действие заблокировано, ожидание{delta} секунд')
            return
        await asyncio.sleep(delta)

        thr = await dispatcher.check_key(key)
        if thr.exceeded_count == thr.exceeded_count:
            await bot.send_message(chat_id=msg.from_user.id, text=f"Доступ к вводу команды")

    async def on_process_message(self, message, data):
        await self.throttle(message)

    async def on_process_callbackquery(self, call, data):
        await self.throttle(call)
