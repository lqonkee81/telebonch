from aiogram import Dispatcher, types

# Машина состояний
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# Database modules
from DataBase import DbHandler
from DataBase import DataBaseExceptions


class FSMstudent(StatesGroup):
    """
    Машина состояния для первоначальной регистрации пользователя
    """
    group = State()
    status = State()

    name = State()
    sorname = State()


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
async def start(messge: types.Message) -> None:
    await messge.answer(text=DESCRIPTION,
                        parse_mode="HTML",
                        # reply_markup=kb_start.get_start_keyboard(),
                        )


# Add user to database
async def setting_up_user(messsage: types.Message) -> None:
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

    except DataBaseExceptions.UserAlreadyExist:
        await messsage.reply("Ты уже зареган")
        print("!!!User already exists!!!")


# Delete user from database
async def delete_user(message: types.Message):
    user_id = message.from_user.id

    try:
        await DbHandler.delete_user(user_id)
        await message.answer("Удалил")

    except DataBaseExceptions.UserDoesNotExist:
        await message.answer("Тебя и так не было")


def register_handlers_student(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start", "help"])
    dp.register_message_handler(setting_up_user, commands=["setme"])
    dp.register_message_handler(delete_user, commands=['delme'])
