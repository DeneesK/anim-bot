import asyncio

from aiogram import Bot, Dispatcher

from src.settings.const import BOT_TOKEN
from src.settings.config import register_all_services
from src.settings.logger import logger


async def main():
    logger.info("Starting Bot")

    bot = Bot(BOT_TOKEN, parse_mode="HTML")

    dp = Dispatcher(bot)
    await register_all_services(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.bot.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped")
