import sqlite3
from os.path import join, isfile


DATABASE_PATH = 'animal.db'
SQL_DIR_PATH = 'sql'
INIT_MIGRATION_FILE_PATH = 'init.sql'
DATA_MIGRATION_FILE_PATH = 'migrate.sql'


def get_sql_from_file(file_name):
    """
    Получает чистый sql из файла.
    :param file_name: путь до файла с данными.
    :return: строку с запросами.
    """
    content = ''
    if isfile(file_name):
        with open(file_name) as file:
            content = file.read()

    return content


def main():
    """
    Выполняет миграцию данных.
    """
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()

        init_sql = get_sql_from_file(join(SQL_DIR_PATH, INIT_MIGRATION_FILE_PATH))
        cursor.executescript(init_sql)

        data_sql = get_sql_from_file(join(SQL_DIR_PATH, DATA_MIGRATION_FILE_PATH))
        cursor.executescript(data_sql)


if __name__ == "__main__":
    main()
