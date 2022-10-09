'''
Очень нужный и важный бот.
Умеет пока что нихуя

Будет уметь:
1. Присылать расписание
2. Если получится, то будет уметь отмечаться за тебя на паре ( но вот как это сделать я хуй его знает )
'''

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    '''
    Сюда надо будет написать всю хелпу
    '''
    await message.answer("Hello")


#
@dp.message_handler(commands=['расписание'])
async def send_raspis(message: types.Message):
    '''
    Вот сюда нужно запихнуть вывод парсера, который должен наклипать Володя.
    Надо будет его пнуть в скором времени
    '''
    await message.answer(text="Падажжи, это пока что не работает")


@dp.message_handler()
async def echo_send(messge: types.Message):
    '''
    Обработка неизвестных комманд
    '''
    await messge.answer("Не понял, что ты хочешь от меня")


executor.start_polling(dp, skip_updates=True)
