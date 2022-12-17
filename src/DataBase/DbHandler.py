import sqlite3

from DataBase import DataBaseExceptions
from UserModels import User

DATA_BASE_PATH = "../DATABASE/db.db"


async def registration_user(user_id: int, user_group: str, user_status: str):
    """
    Занимается регистрацией пользователя в базе данных

    :param user_id: id пользователя
    :param user_group: группа пользователя
    :param user_status: статус пользователя ( студен/староста/преподаватель )
    :return: Ничего
    """

    global DB
    global CURSOR

    user = User.User(user_id, user_group, user_status)

    if (user.get_status().lower() == "студент") or (user.get_status().lower() == "староста"):
        '''
        Регистрация студента/старосты
        '''

        CURSOR.execute(f"SELECT id FROM users WHERE id = {user.get_id()}")
        if CURSOR.fetchone() is None:
            CURSOR.execute("INSERT INTO users VALUES (?, ?, ?);", (user.get_id(),
                                                                   user.get_group(),
                                                                   user.get_status()
                                                                   )
                           )
            DB.commit()
        else:
            print("User already exists")
            raise DataBaseExceptions.UserAlreadyExist
    else:
        raise Exception()


async def delete_user(user_id: int) -> None:
    """
    Удаление пользователя из базы данных

    :param user_id: Id пользователя
    :return: None
    """

    CURSOR.execute(f"SELECT id FROM users WHERE id = {user_id}")
    if CURSOR.fetchone() is not None:
        CURSOR.execute(f"""DELETE from users WHERE id = {user_id}""")
        DB.commit()

    else:
        print("User doesn't exists")
        raise DataBaseExceptions.UserDoesNotExist


async def get_user_group(user_id: int) -> str:
    """
    Получение группы пользователя из базы данных

    :param user_id: Id пользователя
    :return:
    """

    CURSOR.execute(f"SELECT s_group FROM users WHERE id = {user_id}")
    userGroup = CURSOR.fetchone()
    if userGroup:
        return userGroup[0]

    else:
        raise DataBaseExceptions.UserDoesNotExist


def get_full_data_base() -> list:
    """
    :return: Список всех записей в базе данных
    """
    db_as_list = []

    CURSOR.execute("SELECT * FROM users")
    rows = CURSOR.fetchall()
    for i in rows:
        db_as_list.append(i)

    return db_as_list


async def is_user_exists(userId: str) -> bool:
    """

    :param userId:
    :return:
    """

    CURSOR.execute("SELECT id FROM users WHERE id=(?)", userId)
    answer = CURSOR.fetchone()
    if not answer is None:
        return True
    else:
        return False


if __name__ != "__main__":
    DB = sqlite3.connect(DATA_BASE_PATH)
    CURSOR = DB.cursor()

    CURSOR.execute("""CREATE TABLE IF NOT EXISTS users (
                id BIGINT,
                s_group TEXT,
                status TEXT
            )""")
    DB.commit()

else:
    print("bad")
