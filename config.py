import sqlite3
from typing import NamedTuple


HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
DATABASE_NAME = "etks.db"
TABLE_NAME = "professions"


class Connection(NamedTuple):
    db: sqlite3.Connection
    cursor: sqlite3.Cursor

class Profession(NamedTuple):
    name: str
    level: int
    direction: str
    description: str
    requirements: str
