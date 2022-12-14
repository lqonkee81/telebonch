"""
Обработчик сообщений от студента
"""

from aiogram import Dispatcher, types


import keyboards
from DataBase import DataBaseExceptions
from DataBase import DbHandler

from Parser import ScheduleStudentParser
from Parser import ScheduleProfesorParser

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


# Help command handler
async def help(messge: types.Message) -> None:
    await messge.answer(text=DESCRIPTION,
                        parse_mode="HTML",
                        reply_markup=keyboards.kb_start.get_keyboard(),
                        )


async def delete_user(message: types.Message) -> None:
    """
    Стучится в базу с просьбой удалить пользователя

    :param message:
    :return:
    """
    user_id = message.from_user.id

    try:
        await DbHandler.delete_user(user_id)
        await message.answer("Удалил")

    except DataBaseExceptions.UserDoesNotExist:
        await message.answer("Тебя и так не было")


async def get_schudule(messge: types.Message) -> None:
    try:
        # userGroup = await DbHandler.get_user_group(messge.from_user.id)
        parser = ScheduleStudentParser(await DbHandler.get_user_group(messge.from_user.id))
        schedule = await parser.get_week_schedule()
        await messge.answer(text=schedule,
                            parse_mode="HTML")
    except DataBaseExceptions.UserDoesNotExist:
        await messge.answer(text="Тебя нет в базе\nЛибо группа указа неверно")


async def prof_shedule(message: types.Message) -> None:
    # try:
    #     words = list(map(str, message.text.split()))
    #     soname = words[0]
    #     profsList = await Parser.ScheduleProfesorParser.get_all_proffesors_sonames()
    #
    #     if soname in profsList:
    #         sch = await Parser.ScheduleProfesorParser.get_profersor_schedule(soname)
    #
    # except:
    #     print("Something went wrong")
    pp = ScheduleProfesorParser(message.text)
    await message.answer(str(await pp.get_profersor_schedule()))


def register_handlers_student(dp: Dispatcher):
    dp.register_message_handler(help, commands=["help"])
    dp.register_message_handler(delete_user, commands=['delme'])
    dp.register_message_handler(get_schudule, commands=['расписание'])
    dp.register_message_handler(prof_shedule)
