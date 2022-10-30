from datetime import date

from bs4 import BeautifulSoup as BS
import requests

HTML_FILE = "src.html"
GROUPS_LIST = list()


def __today_date() -> str:
    """
    Возаращает дату в человеческом виде
    """

    year, month, day = str(date.today()).split('-')

    return str(day + '.' + month + '.' + year)


def __get_html() -> None:
    """
    Получает разметку и сохраняет ее в файл

    :return: Ничего не возвращает
    """
    HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    }

    GROUPS_URL = "https://www.sut.ru/studentu/raspisanie/raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya"

    html = requests.get(url=GROUPS_URL, headers=HEADERS)
    # __write_html_to_file(html.text)

    with open(HTML_FILE, 'w') as scr:
        scr.write(html.text)


def ParseGroups() -> None:
    """
    Получает список назавний факультетов и содержащихся в них групп

    :rtype: object
    :return: Ничего не возвращет
    """

    with open(HTML_FILE, 'r') as src:
        html = src.read()

    soup = BS(html, "lxml")

    for tables in soup.find_all(class_="vt252"):
        facultName = tables.find(class_="vt253").text.strip()  # Имя факультета
        groupsList = list()

        for i in tables.find_all_next('a', href=True):
            groupId = i["href"]
            groupsList.append({"group_name": i.text.strip(),
                               "group_id": groupId})

        GROUPS_LIST.append((facultName, groupsList))

    return GROUPS_LIST


if __name__ == "__main__":
    # __get_html()
    ParseGroups()

    for i in GROUPS_LIST:
        print(i)
