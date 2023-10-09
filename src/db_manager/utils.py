import psycopg2

from configparser import ConfigParser
from src.api.hh_api import HHApi
from src.employers_list import employers


def config(filename="database.ini", section="postgresql") -> dict:
    """
    Получает данные для подключения к базе данных
    :param filename: файл с данными конфигурации
    :param section: название раздела файла конфигурации
    :return: словарь с параметрами конфигурации
    """
    parser = ConfigParser()

    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        db = dict(params)
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о каналах и видео."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id INTEGER PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                employer_url TEXT
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INTEGER REFERENCES employers(employer_id),
                position VARCHAR NOT NULL,
                min_salary INTEGER,
                max_salary INTEGER,
                requirements TEXT,
                vacancy_url TEXT
            )
        """)

    conn.commit()
    conn.close()


def save_employers(database_name, params):
    conn = psycopg2.connect(dbname=database_name, **params)

    api = HHApi()

    for emp in employers.keys():
        inf = api.get_employer_by_id(emp)
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO employers (employer_id, name, employer_url)
                VALUES (%s, %s, %s)
                """,
                (inf.get('id'), inf.get('name'), inf.get('url'))
            )

    conn.commit()
    conn.close()


def save_vacancies(database_name, params):
    conn = psycopg2.connect(dbname=database_name, **params)

    api = HHApi()

    for emp in employers.keys():
        vacancies = api.get_vacancies_by_company(emp)
        for inf in vacancies:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO vacancies (employer_id, position, min_salary, max_salary, requirements, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (emp, inf.get('position'), inf.get('min_salary'), inf.get('max_salary'),
                     inf.get('requirements'), inf.get('url'))
                )

    conn.commit()
    conn.close()
