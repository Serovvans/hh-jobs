import os
import psycopg2

from src.db_manager.utils import config, create_database, save_employers, save_vacancies


class DBManager:
    """Менеджер для работы с базой данных"""
    def __init__(self, name):
        file_path = os.path.join("src", "db_manager", "database.ini")
        self.__name = name
        self.__params = config(filename=file_path)
        create_database(name, self.__params)
        save_employers(name, self.__params)
        save_vacancies(name, self.__params)

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        query = """
            SELECT employers.name, COUNT(*)
            FROM vacancies
            RIGHT JOIN employers USING(employer_id)
            GROUP BY employers.name
        """
        conn = psycopg2.connect(dbname=self.__name, **self.__params)

        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()

        conn.commit()
        conn.close()
        return data

    def get_all_vacancies(self):
        query = """
            SELECT employers.name, position, min_salary, vacancy_url
            FROM vacancies
            JOIN employers USING(employer_id)
        """

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass
