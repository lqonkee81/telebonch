from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

START_BUTTONS = sorted(["/Расписание", "/Kek"])


def get_start_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True
                                   )
    for i in START_BUTTONS:
        keyboard.add(i)

    return keyboard
