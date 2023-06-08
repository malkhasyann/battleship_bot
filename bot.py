import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_reader import config

from handlers import cmd_handlers
from new_models import matches


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    
    # dp.include...
    
    dp.include_router(cmd_handlers.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, matches = matches.Matches())
    
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())