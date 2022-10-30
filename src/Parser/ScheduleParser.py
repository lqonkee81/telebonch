from datetime import date

import requests
from bs4 import BeautifulSoup as bs

from src.Parser import GroupsParser
from src.Schedule import Lesson, Schedule


def __make_url(userGroup) -> str:
    """
    Формирует адресс запроса для дальнейшего парсинга

    :param userGroup: Учебная группа пользователя
    :return: Урл на страницу с распианием группы пользователя
    """
    groupsList = GroupsParser.getGroupsList()
    groupLink = "https://www.sut.ru/studentu/raspisanie/raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya"

    for i in groupsList:
        for j in i[1]:
            if j.get("group_name") == userGroup:
                groupLink += j.get("group_id")

    groupLink += "&date=" + str(date.today())
    groupLink += "&date=" + "2022-10-31"
    return groupLink


def __get_html(userGroup: str) -> None:
    """
    Получает разметку страницы и сохраняет ее в файл

    :param userGroup: Учебная группа пользователя
    :return: Ничего не возвращает
    """
    URL = __make_url(userGroup)

    HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    }

    html = requests.get(url=URL, headers=HEADERS)
    htmlPath = "../../files/" + userGroup + "_schedule.html"

    with open(htmlPath, 'w') as src:
        src.write(html.text)


def getWeekSchudule(userGroup: str) -> list:
    # __get_html(userGroup)
    htmlPath = "../../files/" + userGroup + "_schedule.html"

    with open(htmlPath, 'r') as src:
        html = src.read()

    soup = bs(html, "lxml")

    for dayNumber in range(1, 7):
        lessons = soup.find("div", class_="vt236").find_all(class_=f"vt239 rasp-day rasp-day{dayNumber}")
        lessonNumber = soup.find_all("div", class_="vt283")  # Номер занятия по порядку

        number = -1
        for lesson in lessons:
            number += 1
            lesName = lesson.find("div", class_="vt240")  # название предмета
            teacherName = lesson.find("span", class_="teacher")  # имя преподавателя
            audinceNumber = lesson.find("div", class_="vt242")  # нормер аудитории
            lesType = lesson.find("div", class_="vt243 vt243b")  # тип занятия
            weekDay = lesson.find_parent("div", class_="vt238")

            if lesType == None:
                lesType = lesson.find("div", class_="vt243 vt243a")

            if lesType == None:
                lesType = lesson.find("div", class_="vt243")

            if lesName != None:
                print("DAYNUMBER: ", weekDay)
                print(lessonNumber[number].text.strip())
                print(lesName.text.strip())
                print(teacherName.text.strip())
                print(audinceNumber.text.strip()[6::])
                print(lesType.text.strip())
                print()

                print()

    return list()


if __name__ == "__main__":
    getWeekSchudule("ИБС-11")
