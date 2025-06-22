import asyncio

from aiogram.types import BotCommand
from shared.config import logger
from bot.handlers import dp, bot


async def set_bot_commands():
    """Установка команд бота"""
    commands = [
        BotCommand(command="start", description="Начать работу с ботом"),
        BotCommand(command="clear", description="Очистить контекст разговора"),
        BotCommand(command="help", description="Получить помощь"),
    ]
    await bot.set_my_commands(commands)


async def main():
    logger.info("Starting Telegram bot...")

    await set_bot_commands()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())