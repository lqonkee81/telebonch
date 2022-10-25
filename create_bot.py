from aiogram import Bot, Dispatcher
import config

if __name__ != "__main__":
    BOT = Bot(config.TOKEN)
    DP = Dispatcher(BOT)
