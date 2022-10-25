from datetime import date
from Schedule import Schedule

from bs4 import BeautifulSoup as BS
import requests

groups_url = "https://www.sut.ru/studentu/raspisanie/raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya"
groups = requests.get(url=groups_url)

soup = BS(groups, "lxml")


def __today_date() -> str:
    """
    Возаращает дату в человеческом виде
    """

    year, month, day = str(date.today()).split('-')

    return str(day + '.' + month + '.' + year)


def get_groups() -> list:
    groups = []

    return groups


def get_schedule(group: str, week: str) -> Schedule:
    pass


if __name__ == "__main__":
    print(soup.tagStack)
