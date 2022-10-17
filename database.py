import sqlite3

from config import DATABASE_NAME, TABLE_NAME, Profession, Connection


def connect_to_db() -> Connection:
    db = sqlite3.connect(DATABASE_NAME)
    return Connection(db, db.cursor())

def create_table(table_name: str = TABLE_NAME) -> None:
    db, cursor = connect_to_db()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        direction VARCHAR(255),
        profession VARCHAR(255),
        level INTEGER,
        description TEXT,
        skills TEXT)""")
    db.commit()
    db.close()

def add_profession(data: Profession, table_name: str = TABLE_NAME) -> None:
    db, cursor = connect_to_db()
    cursor.execute(f"""INSERT INTO {table_name} (direction, profession, level, description, skills) VALUES(?,?,?,?,?)""", 
        (data.direction, data.name, data.level, data.description, data.requirements))
    db.commit()
    db.close()
    print("Успешно записали в БД:", data.name)

def get_all_professions(table_name: str = TABLE_NAME) -> list[Profession]:
    db, cursor = connect_to_db()
    cursor.execute(f"SELECT * FROM {table_name}")
    professions = (Profession(*row[1:]) for row in cursor.fetchall()) # [1:] Ignore db id
    return professions

if __name__ == "__main__":
    get_all_professions()
