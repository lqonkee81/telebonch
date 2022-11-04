from aiogram.types import ReplyKeyboardMarkup

START_BUTTONS = sorted(["/delme", "/Расписание"])


def get_start_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True
                                   )
    for i in START_BUTTONS:
        keyboard.add(i)

    return keyboard
