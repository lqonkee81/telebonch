import os.path
import asyncio
from datetime import date
from datetime import datetime

import requests
from bs4 import BeautifulSoup as BS

import Parser.GroupsParser
from Parser import GroupsParser
from Schedule import StudentDaySchedule
from Schedule import StudentLesson
from Schedule import WeekStudentSchedule

DEGUB = True


async def __get_bonch_week_number():
    day, month = datetime.now().day, datetime.now().month

    firstStydyWeek = date(datetime.now().year, 9, 1).isocalendar()[1]  # Номер первой учебной недели в году
    weekNumberInYear = date(datetime.now().year, int(month), int(day)).isocalendar()[
                           1] + 1  # Номер недели на текущий момент
    bonchWeek = weekNumberInYear - firstStydyWeek

    return bonchWeek


async def __get_html_path(userGroup, weekNum=None) -> str:
    """
    Путь до файла с разметкой с расписанием

    :param userGroup: Учебная группа пользователя
    :return: Путь до файла с расписанием
    """
    checkPathFolder = f"../files/Schedules/Students/{userGroup}"

    if not os.path.exists(checkPathFolder):
        """Проверяем существует ли папка группы с расписаниями"""
        os.mkdir(checkPathFolder)

    if weekNum is None:
        weekNum = await __get_bonch_week_number()

    html_path = f"{checkPathFolder}/sch_{weekNum}.html"  # Путь до файла с расписанием
    return html_path


async def __make_url(userGroup: str, scheduleDate=None) -> str:
    """
    Формирует адресс запроса для дальнейшего парсинга

    :param userGroup: Учебная группа пользователя
    :return: Урл на страницу с распианием группы пользователя
    """
    if DEGUB:
        print("DEBUG: SCHEDULE_PARSER -> __make_url")

    facultsList = await GroupsParser.getGroupsList()
    groupLink = "https://www.sut.ru/studentu/raspisanie/raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya"

    for facult in facultsList:
        group = facult.get_group_by_name(userGroup)

        if group != None:
            if DEGUB:
                print(group)
            groupLink += group.id
            break

    if scheduleDate is None:
        scheduleDate = str(date.today())

    print(f"TODAY DATE: {scheduleDate}")
    groupLink += "&date=" + scheduleDate

    if DEGUB:
        print(groupLink)

    return groupLink


async def __get_html(userGroup: str, weekNum=None) -> None:
    """
    Получает разметку страницы и сохраняет ее в файл

    :param userGroup: Учебная группа пользователя
    :return: Ничего не возвращает
    """

    htmlPath = await __get_html_path(userGroup, weekNum)

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


async def get_week_schedule(userGroup: str, weekNumber=None, name=None) -> str:
    """
    Парсит расписание на неделю
    :param userGroup: Группа пользователя
    :return: Schedule ( по факту расписание кароч )
    """
    if DEGUB:
        msg = "DEBUG: SCHEDULE_PARSER -> get_week_schudule"
        print(f"{msg:.^20}")

    htmlPath = await __get_html_path(userGroup, weekNumber)

    if not os.path.exists(htmlPath):
        """ Проверяем существует-ли готовый файл с расписанием """
        await __get_html(userGroup)

    with open(htmlPath, 'r') as src:
        html = src.read()

    soup = BS(html, "lxml")

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
    numbers = list()
    for i in lines:
        tmp = i.find_next("div", class_="vt239")
        times.append(str(tmp.contents[2]) + '-' + str(tmp.contents[4]))
        numbers.append(tmp.contents[0].text)

    days = list()
    lessList = list()
    for i in range(0, len(daysList)):
        lessList.clear()
        scheduleDay = soup.find_all("div", class_=f"vt239 rasp-day rasp-day{i + 1}")

        for lesson in range(len(scheduleDay)):

            lesName = scheduleDay[lesson].find("div", class_="vt240")  # Название занятия
            lesProfessor = scheduleDay[lesson].find("span", class_="teacher")  # Имя преподователя
            audinceNumber = scheduleDay[lesson].find("div", class_="vt242")  # Номер аудитории занятия
            lesType = scheduleDay[lesson].find("div", class_="vt243 vt243b")  # Тип занятия

            if lesType == None:
                lesType = scheduleDay[lesson].find("div", class_="vt243 vt243a")

            if lesType == None:
                lesType = scheduleDay[lesson].find("div", class_="vt243")

            if lesName is not None:
                if name is None:
                    les = StudentLesson.Lesson(name=lesName.text.strip(),
                                        time=times[lesson],
                                        audienceNumber=audinceNumber.text.strip(),
                                        proffesorName=lesProfessor.text.strip(),
                                        type=lesType.text.strip(),
                                        number=numbers[lesson])
                    lessList.append(les)
                else:
                    if lesProfessor.text.strip() == name:
                        les = StudentLesson.Lesson(name=lesName.text.strip(),
                                            time=times[lesson],
                                            audienceNumber=audinceNumber.text.strip(),
                                            proffesorName=lesProfessor.text.strip(),
                                            type=lesType.text.strip(),
                                            number=numbers[lesson])
                        lessList.append(les)

        scD = StudentDaySchedule.DaySchedule(weekDay=6 * '=' + daysList[i].upper() + 6 * '=',
                                      lessonsList=lessList.copy())
        days.append(scD)

    schedule = WeekStudentSchedule.WeekSchedule(days)

    return str(schedule)


async def get_all_groups_html():
    groupsList = await Parser.GroupsParser.getGroupsList()
    return str(groupsList)


if __name__ == "__main__":
    asyncio.run(get_all_groups_html())
else:
    global SCHEDULE_DAY_PATH, SCHEDULE_WEEK_PATH
