import sqlite3

from config import DATABASE_NAME, TABLE_NAME, Profession, Connection


def connect_to_db() -> Connection:
    db = sqlite3.connect(DATABASE_NAME)
    return Connection(db, db.cursor())

def create_table() -> None:
    db, cursor = connect_to_db()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        direction VARCHAR(255),
        profession VARCHAR(255),
        level INTEGER,
        description TEXT,
        skills TEXT)""")
    db.commit()
    db.close()

def add_profession(data: Profession) -> None:
    db, cursor = connect_to_db()
    cursor.execute(f"""INSERT INTO {TABLE_NAME} (profession, level, direction, description, skills) VALUES(?,?,?,?,?)""", (*data, ))
    db.commit()
    db.close()
    print("Успешно записали в БД:", data.name)