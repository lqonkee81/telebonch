from aiogram import executor
from create_bot import DP

# Работа с базой данных
from DataBase import DbHandler

# Обработчики сообщений
from handlers import student, other

student.register_handlers_student(DP)
other.register_handlers_other(DP)


# Startup function
async def get_ready(_):
    print("-------------------------Bot is started-------------------------")

    print("DATA BASE: ")

    bd = DbHandler.get_full_data_base()
    for i in bd:
        print(i)


# Shutdown function
async def shutdown(_):
    print("-------------------------Bot is stopped-------------------------")


if __name__ == "__main__":
    executor.start_polling(dispatcher=DP,
                           skip_updates=True,
                           on_startup=get_ready,
                           on_shutdown=shutdown,

                           )
