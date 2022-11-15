from aiogram import executor

from DataBase import DbHandler
from create_bot import DP, BOT
from handlers import student, other, registration

registration.register_register_handlers(DP)
student.register_handlers_student(DP)
other.register_handlers_other(DP)


# Startup function
async def get_ready(_):
    users = DbHandler.get_full_data_base()

    for user in users:
        userId = user[0]
        # await BOT.send_message(userId, text="Я снова работаю")

    print(users)

    print("-------------------------Bot is started-------------------------")


# Shutdown function
async def shutdown(_):
    users = DbHandler.get_full_data_base()
    print(users)

    for user in users:
        userId = user[0]
        await BOT.send_message(userId, text="Сайонара. Я на ТО")

    print("-------------------------Bot is stopped-------------------------")


if __name__ == "__main__":
    executor.start_polling(dispatcher=DP,
                           skip_updates=True,
                           # on_startup=get_ready,
                           # on_shutdown=shutdown,
                           )