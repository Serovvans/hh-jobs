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

    def __execute_data_from_db(self, query: str) -> list[tuple]:
        """
        Выполняет SELECT-запросы и возвращает полученные данные
        :param query: текст запроса
        :return: данные по запросу
        """
        conn = psycopg2.connect(dbname=self.__name, **self.__params)

        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()

        conn.commit()
        conn.close()
        return data

    @staticmethod
    def __put_vacancy_to_dict(data: list[tuple]) -> list[dict]:
        """
        Формирует словарь с информацией о вакансии
        :param data: список картежей ваканисий
        :return: словарь вакансий
        """
        answer = [{"employer": item[0],
                   "position": item[1],
                   "min_salary": item[2],
                   "url": item[3]} for item in data]

        return answer

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """
        Возвращает список всех компаний и их количество вакансий
        :return: список картежей с названием компании и количеством вакансий
        """
        query = """
            SELECT employers.name, COUNT(*)
            FROM vacancies
            RIGHT JOIN employers USING(employer_id)
            GROUP BY employers.name
        """
        data = self.__execute_data_from_db(query)

        return data

    def get_all_vacancies(self) -> list[dict]:
        """
        :return: список всех вакансий с указанием названия компании
        """
        query = """
            SELECT employers.name, position, min_salary, vacancy_url
            FROM vacancies
            JOIN employers USING(employer_id)
        """
        data = self.__execute_data_from_db(query)
        return self.__put_vacancy_to_dict(data)

    def get_avg_salary(self) -> float:
        """
        :return: средняя минимальная зарплата по всем вакансиям
        """
        query = "SELECT AVG(min_salary) FROM vacancies"

        data = self.__execute_data_from_db(query)
        return data[0][0]

    def get_vacancies_with_higher_salary(self) -> list[dict]:
        """
        :return: список вакансий с минимальной зарплатой выше среднего значения
        """
        query = """
            SELECT employers.name, position, min_salary, vacancy_url FROM vacancies
            JOIN employers USING(employer_id)
            WHERE min_salary > (SELECT AVG(min_salary) FROM vacancies)
        """
        data = self.__execute_data_from_db(query)
        return self.__put_vacancy_to_dict(data)

    def get_vacancies_with_keyword(self, key: str) -> list[dict]:
        """
        :param key: ключевой слово для поиска вакансии
        :return: список вакансий, содержащий ключевое слова
        """
        query = f"""
            SELECT employers.name, position, min_salary, vacancy_url FROM vacancies
            JOIN employers USING(employer_id)
            WHERE vacancies.position LIKE '%{key}%'
        """
        data = self.__execute_data_from_db(query)
        return self.__put_vacancy_to_dict(data)
