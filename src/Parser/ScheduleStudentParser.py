import os.path
from datetime import date
from datetime import datetime

import requests
from bs4 import BeautifulSoup as BS

import Parser.GroupsParser
from Logger import Logger
from Parser import GroupsParser
from Schedule import StudentDaySchedule
from Schedule import StudentLesson
from Schedule import WeekStudentSchedule


class ScheduleStudentParser:
    def __init__(self, userGroup: str, date = None):
        self.DEBUG = False
        self.logger = Logger()

        self.userGroup = userGroup
        self.date = date
        if self.date is None:
            self.scheduleDate = str(date.today())
        else:
            self.scheduleDate = date

        self.__HEADERS = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        }

        self.folderWithHtmls = "../files/Schedules/Students/"
        self.userHtmlFolder = self.folderWithHtmls + userGroup + '/'
        self.html = self.userHtmlFolder + "sch_" + str(self.get_bonch_week_number()) + ".html"

        self.url = str(self.__make_url())
        self.create_directories()

    def create_directories(self):
        if not os.path.exists("../files"):
            os.mkdir("../files")
            self.logger.warning("Was created directory '../files'", __name__)

        if not os.path.exists("../files/Schedules"):
            os.mkdir("../files/Schedules")
            self.logger.warning("Was created directory '../files/Schedules'", __name__)

        if not os.path.exists(self.folderWithHtmls):
            os.mkdir(self.folderWithHtmls)
            self.logger.warning(f"Was created directory {self.folderWithHtmls}", __name__)

        if not os.path.exists(self.userHtmlFolder):
            os.mkdir(self.userHtmlFolder)
            self.logger.warning(f"Was created directory {self.userHtmlFolder}", __name__)

    def get_bonch_week_number(self):
        day, month = datetime.now().day, datetime.now().month

        if 1 <= datetime.now().month <= 8:
            year = datetime.now().year - 1
        else:
            year = datetime.now().year

        # firstStudyWeek = date(datetime.now().year - 1, 9, 1).isocalendar()[1]  # Номер первой учебной недели в году
        firstStudyWeek = date(year, 9, 1).isocalendar()[1]  # Номер первой учебной недели в году
        weekNumberInYear = date(year, int(month), int(day)).isocalendar()[1] + 1  # Номер недели на текущий момент
        additionalWeeks = date(year, 12, 31).isocalendar()[1] # Исправляет баг при переходе к новому году
        bonchWeek = (weekNumberInYear + additionalWeeks) - firstStudyWeek

        return bonchWeek

    def __make_url(self) -> str:
        """
        Формирует адресс запроса для дальнейшего парсинга

        :param userGroup: Учебная группа пользователя
        :return: Урл на страницу с распианием группы пользователя
        """
        self.logger.info("Making url", __name__)

        groupLink = "https://www.sut.ru/studentu/raspisanie/raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya"
        gp = GroupsParser()
        facultsList = gp.get_facults_list()

        for facult in facultsList:
            group = facult.get_group_by_name(self.userGroup)

            if group != None:
                if self.DEBUG:
                    print(group)
                groupLink += group.id
                break

        groupLink += "&date=" + self.scheduleDate

        if self.DEBUG:
            print(groupLink)

        return groupLink

    async def __download_html(self) -> None:
        """
        Получает разметку страницы и сохраняет ее в файл

        :param userGroup: Учебная группа пользователя
        :return: Ничего не возвращает
        """

        self.logger.info(f"Downloading html for{self.userGroup}", __name__)

        html = requests.get(url=self.url, headers=self.__HEADERS)
        with open(self.html, 'w') as src:
            src.write(html.text)

    async def get_week_schedule(self) -> str:
        """
        Парсит расписание на неделю
        :param userGroup: Группа пользователя
        :return: Schedule ( по факту расписание кароч )
        """
        self.logger.info(f"Getting week schedule for {self.userGroup}", __name__)

        if self.DEBUG:
            msg = "DEBUG: SCHEDULE_PARSER -> get_week_schudule"
            print(f"{msg:.^{len(msg) + 6}}")

        if not os.path.exists(self.html):
            await self.__download_html()

        with open(self.html, 'r') as src:
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
                    les = StudentLesson.StudentLesson(name=lesName.text.strip(),
                                                      time=times[lesson],
                                                      audienceNumber=audinceNumber.text.strip(),
                                                      proffesorName=lesProfessor.text.strip(),
                                                      type=lesType.text.strip(),
                                                      number=numbers[lesson])
                    lessList.append(les)

            scD = StudentDaySchedule(weekDay=6 * '=' + daysList[i].upper() + 6 * '=',
                                                        lessonsList=lessList.copy())
            days.append(scD)

        schedule = WeekStudentSchedule.StudentWeekSchedule(days)

        return str(schedule)

    async def get_all_groups_html(self):
        groupsList = await Parser.GroupsParser.getGroupsList()
        return str(groupsList)


if __name__ == "__main__":
    gp = GroupsParser()

    for i in gp:
        ssp = ScheduleStudentParser(userGroup=i,
                                    date="2022-11-28")