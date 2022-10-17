import database
import xlrd
import os

from config import Profession, TABLE_WITH_EDWICA_PROF


def merge_professions(groups: list[list[Profession]]) -> list[list[Profession]]:
    """Нужно выделить среди всех одинаковых профессий разных уровней нулевую профессию.
    В описании и навыки которой засунуть сумму остальных одинаковых профессий
    Еще нужно изменить название добавив туда уровень разряда
    Пример: Профессия: Маляр, Уровень:3 -> Название: Маляр (3 разряда), Уровень: 3"""
    for group in groups:
        # Добавляем в группу нулевую профессию, содержащую сумму описаний и сумму требований
        zero_profession_title = group[0].name
        zero_profession_direction = group[0].direction
        zero_profession_descr = "|".join((proff.description for proff in group))
        zero_profession_skills = "|".join((proff.requirements for proff in group))

        database.add_profession(Profession(zero_profession_direction, zero_profession_title, 0, zero_profession_descr, zero_profession_skills), TABLE_WITH_EDWICA_PROF)

        for proff in group: # Меняем наименования профессий, добавляя к ним уровень разряда
            proff.name = f"{proff.name} ({proff.level} разряда)"
            database.add_profession(proff, TABLE_WITH_EDWICA_PROF)


def group_professions(professions: list[Profession]) -> list[list[Profession]]:
    """Объединяем в группу профессии, у которых одинаковые названия, но разные уровни
    Это нужно чтобы было проще добавлять нулевые профессии, т.к в описании нулевой профессии должны быть описания всех уровней"""

    group_profession_by_title = []
    for profession in professions:
        if profession.name in (group[0].name for group in group_profession_by_title):
            for group in group_profession_by_title:
                if profession.name == group[0].name: group.append(profession)
        else:
            group_profession_by_title.append([profession, ])
    return group_profession_by_title


def read_edwica_professions(professions_folder_path:str):
    for ex_file in os.listdir(professions_folder_path):
        if ex_file.endswith(".xlsx"):
            document = os.path.join(professions_folder_path, ex_file)
            book = xlrd.open_workbook(document)
            direction_sheet = book.sheet_by_name("Список профессий")
            descr_sheet = book.sheet_by_name("Функции (общие)")
            skill_sheet = book.sheet_by_name("Навыки")


            #professions = (item for item in prof_sheet.col_values(5) if item)
            for row in range(1, descr_sheet.nrows):
                Title = descr_sheet.row_values(row)[1] # Колонка "Название 2-ого уровня"
                Descrs = "|".join(descr for descr in descr_sheet.row_values(row)[2:] if descr)
                for row2 in range(1, skill_sheet.nrows):
                    if Title == skill_sheet.row_values(row2)[1]:
                        Skills = "|".join(skill for skill in skill_sheet.row_values(row2)[2:] if skill)
                for row3 in range(1, direction_sheet.nrows):
                    if Title == direction_sheet.row_values(row3)[5]:
                        Direction = direction_sheet.row_values(row3)[3] # Колонка "Направление"
                profession = Profession(Direction, Title, 0, Descrs, Skills)
                database.add_profession(profession, TABLE_WITH_EDWICA_PROF)

            break


def main():
    database.create_table(TABLE_WITH_EDWICA_PROF)
    professions = database.get_all_professions()
    groups = group_professions(professions)
    # Начинаем запись в БД
    merge_professions(groups)
    read_edwica_professions("/home/saloman/Documents/Профессии(14.10.2022)")

if __name__ == "__main__":
    main()
