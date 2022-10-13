from bs4 import BeautifulSoup
import requests
import re

import database
from config import HEADERS, Profession


def get_soup(url: str) -> BeautifulSoup:
    req = requests.get(url, headers=HEADERS)
    return BeautifulSoup(req.text, "lxml")


def parse_all_directions() -> None:
    url = "https://classinform.ru/etks.html"
    soup = get_soup(url)
    directions_urls = (item['href'] for item in soup.find("div", attrs={"id": "cont_txt"}).find_all("a") if "Раздел." in item.text)

    for address in directions_urls:
        parse_one_direction(url=address)


def parse_one_direction(url: str) -> None:
    soup = get_soup(url)
    content = soup.find("div", attrs={"id": "cont_txt"})
    direction_title = content.find("h1").text
    has_pagination = True if "Выберите страницу" in content.find_all("p")[-2].text else False

    parse_page(url) # Сохраняем самую первую страницу
    if has_pagination:
        for page in content.find_all("p")[-2].find_all("a"):
            parse_page("http:" + page['href'])


def parse_page(url: str) -> None:
    soup = get_soup(url)
    content = soup.find("div", attrs={"id": "cont_txt"})
    professions = (prof.a['href'] for prof in content.find_all("p")[0:-2:2][1:])
    for prof in professions:
        parse_profession(prof)


def parse_profession(url: str) -> None:
    soup = get_soup("http:" + url)
    content = soup.find("div", attrs={"id": "cont_txt"})

    title = content.find("h1").text
    direction = [item.text for item in content.find_all("p") if "Раздел" in item.text][0].replace("Раздел", "").replace('"', '')
    description_content = content.find_all("p")[-2].text
    description = description_content.split("\n")[0].replace("Характеристика работ.", "").strip()
    skills = description_content.split("\n")[1].replace("Должен знать:", "").strip().capitalize()
    try:level = re.findall("\d+", content.find("h2").text)[0]
    except: level = 0
    database.add_profession(Profession(title, level, direction, description, skills))


if __name__ == "__main__":
    database.create_table()
    parse_all_directions()