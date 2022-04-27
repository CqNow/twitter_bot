import asyncio
import logging
import aioredis
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tg_bot.config import load_config
from tg_bot.filters.admin import AdminFilter
from tg_bot.handlers.admin import register_admin
from tg_bot.middlewares.throttling import ThrottlingMiddleware

logger = logging.getLogger(__name__)


def register_all_middlewares(dp: Dispatcher):
    dp.setup_middleware(ThrottlingMiddleware())


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp: Dispatcher):
    register_admin(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )
    config = load_config('.env')

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    bot['config'] = config

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot Stopped')
