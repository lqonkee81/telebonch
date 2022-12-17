import os.path

import requests
from bs4 import BeautifulSoup as bs

from Parser import Facult
from Parser import Group


class GroupsParser:
    def __init__(self):
        self.HEADERS = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        }

        self.url = "https://www.sut.ru/studentu/raspisanie/raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya"
        self.html = "../files/groups.html"

    def __download_html(self) -> None:
        """
        Получает разметку и сохраняет ее в файл
        """

        html = requests.get(url=self.url, headers=self.HEADERS)

        with open(self.html, 'w') as scr:
            scr.write(html.text)

    def get_facults_list(self) -> Facult:
        """
        Получает список назавний факультетов и содержащихся в них групп

        :rtype: object
        :return: возвращает список групп
        """

        if not os.path.exists(self.html):
             self.__download_html()

        with open(self.html, 'r') as src:
            html = src.read()

        soup = bs(html, "lxml")

        facultsList = list()
        for tables in soup.find_all(class_="vt252"):
            facultName = tables.find(class_="vt253").text.strip()  # Имя факультета
            groupsList = list()

            for i in tables.find_all('a', href=True):
                group = Group.Group(i.text.strip(), i["href"])
                groupsList.append(group)

            facult = Facult.Facult(facultName, groupsList)
            facultsList.append(facult)

        return facultsList
