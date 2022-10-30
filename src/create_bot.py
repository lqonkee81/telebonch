"""
Здесь создается объект бота и диспетчера
"""

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config

if __name__ != "__main__":
    STORAGE = MemoryStorage()

    BOT = Bot(config.TOKEN)
    DP = Dispatcher(bot=BOT,
                    storage=STORAGE)
