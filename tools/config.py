import sqlite3
from dataclasses import dataclass

from pydantic import BaseSettings
from typing import Literal, NamedTuple


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

class Settings(BaseSettings):
    headers: dict[Literal['User-Agent']]
    db_name: str
    table_name: str
    merged_table: str
    excel_folder: str

settings = Settings(
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"},
    "data/sql/etks.db",
    "professions",
    "merged_levels",
    "data/excel"
)
