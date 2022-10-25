from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

TEST_BUTTONS = sorted(['/Расписание', '/Сообщение старосте', '/На_главную'])


def get_test_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                   )
    for i in TEST_BUTTONS:
        keyboard.add(i)

    return keyboard
