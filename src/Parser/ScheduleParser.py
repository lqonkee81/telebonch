import os.path
from datetime import date

import requests
from bs4 import BeautifulSoup as bs

from src.Parser import GroupsParser
from src.Schedule import Lesson
from src.Schedule import Schedule

DEGUB = False


async def __make_url(userGroup: str, scheduleDate=None) -> str:
    """
    Формирует адресс запроса для дальнейшего парсинга

    :param userGroup: Учебная группа пользователя
    :return: Урл на страницу с распианием группы пользователя
    """
    if DEGUB:
        print("\t\t\t\tDEBUG: SCHEDULE_PARSER -> __make_url")

    groupsList = GroupsParser.getGroupsList()
    groupLink = "https://www.sut.ru/studentu/raspisanie/raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya"

    for i in groupsList:
        for j in i[1]:
            if j.get("group_name") == userGroup:
                groupLink += j.get("group_id")

    if scheduleDate == None:
        scheduleDate = str(date.today())

    groupLink += "&date=" + scheduleDate

    return groupLink


async def __get_html(userGroup: str) -> None:
    """
    Получает разметку страницы и сохраняет ее в файл

    :param userGroup: Учебная группа пользователя
    :return: Ничего не возвращает
    """

    htmlPath = "../files/Schedules/" + userGroup + "_schedule.html"

    if DEGUB:
        msg = "DEBUG: SCHEDULE_PARSER -> __get_html"
        print(f'{msg:-^20}')

    URL = await __make_url(userGroup)

    HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    }

    html = requests.get(url=URL, headers=HEADERS)
    with open(htmlPath, 'w') as src:
        src.write(html.text)


async def get_week_schedule(userGroup: str) -> Schedule:
    """
    Парсит расписание на неделю
    :param userGroup: Группа пользователя
    :return: Schedule ( по факту расписание кароч )
    """
    if DEGUB:
        msg = "DEBUG: SCHEDULE_PARSER -> get_week_schudule"
        print(f"{msg:.^20}")

    htmlPath = "../files/Schedules/" + userGroup + "_schedule.html"

    if not os.path.exists(htmlPath):
        """ Проверяем существует-ли готовый файл с расписанием """
        await __get_html(userGroup)

    with open(htmlPath, 'r') as src:
        html = src.read()

    soup = bs(html, "lxml")

    scheduleTable = soup.find("div", class_="vt236")  # Таблицца с расписанием
    weekDaysTable = scheduleTable.find("div", class_="vt244 vt244a")  # Таблица с днями недели и датой
    lines = scheduleTable.find_all("div", class_="vt244")
    lines = lines[1::]

    weekDays = weekDaysTable.find("div", class_="vt237 vt237a").find_all_next("div", class_="vt237")
    daysList = list()

    for day in weekDays:
        wd = day.find_next("div", class_='vt238')

        daysList.append(
            str(day.contents[0].strip()) + ' ' + str(wd.text.strip())
        )

    times = list()
    for i in lines:
        tmp = i.find_next("div", class_="vt239")
        times.append(str(tmp.contents[2]) + '-' + str(tmp.contents[4]))

    ls = list()
    for i in range(0, len(daysList)):
        scheduleDay = soup.find_all("div", class_=f"vt239 rasp-day rasp-day{i + 1}")

        print(daysList[i])
        for lesson in range(len(scheduleDay)):

            lesName = scheduleDay[lesson].find("div", class_="vt240")  # Название занятия
            lesProfessor = scheduleDay[lesson].find("span", class_="teacher")  # Имя преподователя
            audinceNumber = scheduleDay[lesson].find("div", class_="vt242")  # Номер аудитории занятия
            lesType = scheduleDay[lesson].find("div", class_="vt243 vt243b")  # Тип занятия

            if lesType == None:
                lesType = scheduleDay[lesson].find("div", class_="vt243 vt243a")

            if lesType == None:
                lesType = scheduleDay[lesson].find("div", class_="vt243")

            if lesName != None:
                les = Lesson.Lesson(name=lesName.text.strip(),
                                    time=times[lesson],
                                    audienceNumber=audinceNumber.text.strip(),
                                    proffesorName=lesProfessor.text.strip(),
                                    type=lesType.text.strip())
                ls.append(les)

    schedule = Schedule.Schedule(ls)
    return schedule
