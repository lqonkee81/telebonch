import os.path

import requests
from bs4 import BeautifulSoup as bs

# HTML_FILE = "../files/src.html"
HTML_FILE = "../files/groups.html"
GROUPS_URL = "https://www.sut.ru/studentu/raspisanie/raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya"
GROUPS_LIST = list()


async def __get_html() -> None:
    """
    Получает разметку и сохраняет ее в файл
    """

    HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    }

    html = requests.get(url=GROUPS_URL, headers=HEADERS)

    with open(HTML_FILE, 'w') as scr:
        scr.write(html.text)


async def getGroupsList() -> list:
    """
    Получает список назавний факультетов и содержащихся в них групп

    :rtype: object
    :return: возвращает список групп
    """

    if not os.path.exists(HTML_FILE):
        await __get_html()

    with open(HTML_FILE, 'r') as src:
        html = src.read()

    soup = bs(html, "lxml")

    for tables in soup.find_all(class_="vt252"):
        facultName = tables.find(class_="vt253").text.strip()  # Имя факультета
        groupsList = list()

        for i in tables.find_all('a', href=True):
            groupId = i["href"]
            groupsList.append({"group_name": i.text.strip(),
                               "group_id": groupId})

        GROUPS_LIST.append((facultName, groupsList))

    return GROUPS_LIST
