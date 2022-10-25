from aiogram import Bot, Dispatcher, executor, types

# Клавиатуры
from keyboards import *

# Работа с базой данных
from DataBase import DbHandler
import DataBase.DataBaseExceptions

import config

BOT = Bot(config.TOKEN)
DP = Dispatcher(BOT)

DESCRIPTION = """
Этот бот разрабатывается для помощи бедным студентам, дабы те могли как нормальные люди смотреть расписание.

Из будущего функционала:
\t1. Расписание
\t2. Отметка о начале занятия ( но это вряд ли, ибо небезопасно )
\t3. Квик мсг для старосты ( кнопки: заболел, опаздываю, проебываю )
\t4. Мб еще что-то будет. Можешь написать свою мысль в книгу жвлоб и предложений

Команды:  
\t1. <b>/help</b> - <em>Помощь по боту ( данное сообщение )</em>
\t2. <b>/setme ГРУППА СТУДЕНТ/ПРЕПОДАВАТЕЛЬ/СТАРОСТА</b> - <em>Первоначальная настройка бота ( без нее работать ничего не будет )</em>
\t3. <b>/delme</b> - <em>Удаления себя из базы бота</em>
"""


# Start command handler
@DP.message_handler(commands=["start", "help"])
async def start(messge: types.Message) -> None:
    await messge.answer(text=DESCRIPTION,
                        parse_mode="HTML",
                        # reply_markup=kb_start.get_start_keyboard(),
                        )


# Setup user in bot
@DP.message_handler(commands=["setme"])
async def seting_up_user(messsage: types.Message) -> None:
    # Флаг отвественный за валидность данных
    isDataValid = True

    try:
        msg_as_list = list(map(str, messsage.text.split()))
    except:

        return ...

    try:
        if len(msg_as_list) != 3:
            await messsage.reply(text="Необходимо указать группу и свой статус")
            await messsage.answer(text="Например: /setme ВГС-228 студент|староста|преподаватель")
            isDataValid = False
            return ...

        # Проверяем валидность группы ( пока что максимально костыльно, потом перепишем, как только прикрутим бд со всеми группами )
        if '-' not in msg_as_list[1]:
            isDataValid = False
            await messsage.reply(text="Группа указана не верно")

        # Проверяем валидность статуса
        if (msg_as_list[2].lower() != "студент") and \
                (msg_as_list[2].lower() != "староста") and \
                (msg_as_list[2].lower() != "преподаватель"):
            isDataValid = False
            await messsage.reply(text="Статус указан не верно")

        # Здесб после всех проверок происходит регистрация
        if isDataValid:
            user_id = messsage.from_user.id
            user_group = msg_as_list[1]
            user_status = msg_as_list[2]

            await DbHandler.registration_user(user_id, user_group, user_status)
            await messsage.answer("Записал")

        else:
            await messsage.reply(text="Необходимо указать группу и свой статус")
            await messsage.answer(text="Например: /setme ВГС-228 студент|староста|преподаватель")
            return ...

    except DataBase.DataBaseExceptions.UserAlreadyExist:
        await messsage.reply("Ты уже зареган")
        print("!!!User already exists!!!")


@DP.message_handler(commands=['delme'])
async def delete_user(message: types.Message):
    user_id = message.from_user.id

    try:
        await DbHandler.delete_user(user_id)
        await message.answer("Удалил")

    except DataBase.DataBaseExceptions.UserDoesNotExist:
        await message.answer("Тебя и так не было")


# Unknown commands handler
@DP.message_handler()
async def echo(message: types.Message) -> None:
    """
    Удаляет сообщения с рандомным текстом ( рандомный текст - все что не специальная команда бота)
    """
    # await message.delete()
    await message.answer(text=message.text)


# Startup function
async def get_ready(_):
    print("-------------------------Bot is started-------------------------")

    print("DATA BASE: ")

    bd = DbHandler.get_full_data_base()
    for i in bd:
        print(i)


async def shutdown(_):
    print("-------------------------Bot is stopped-------------------------")


if __name__ == "__main__":
    executor.start_polling(dispatcher=DP,
                           skip_updates=True,
                           on_startup=get_ready,
                           on_shutdown=shutdown,

                           )
