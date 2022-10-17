import sqlite3
from dataclasses import dataclass

from typing import NamedTuple

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
DATABASE_NAME = "etks.db"
TABLE_NAME = "professions"
TABLE_WITH_EDWICA_PROF = "final"

class Connection(NamedTuple):
    db: sqlite3.Connection
    cursor: sqlite3.Cursor

@dataclass(slots=True)
class Profession:
    direction: str
    name: int
    level: str
    description: str
    requirements: str

    def __iter__(self):
        return (self.direction, self.name, self.level, self.description, self.requirements)
