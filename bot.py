import asyncio
import subprocess

from aiogram import Bot, Dispatcher

from src.settings.const import BOT_TOKEN, POSTGRES_DSN
from src.settings.config import register_all_services
from src.settings.logger import logger
from src.database import db, cache


async def main():
    # logger.info("APPP STARTING...")
    # subprocess.call(['python3', 'src/app/app.py'])
    logger.info("Starting Bot")

    bot = Bot(BOT_TOKEN, parse_mode='HTML')

    dp = Dispatcher(bot)

    await register_all_services(dp)

    try:
        cache.cache = await cache.setup()
        db.async_session = await db.setup(POSTGRES_DSN)
        await dp.start_polling()
    except Exception as ex:
        logger.error(ex)
        db.async_session.close_all()
        await cache.cache.close()
        return
    finally:
        await dp.bot.close()
        db.async_session.close_all()
        await cache.cache.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped")
