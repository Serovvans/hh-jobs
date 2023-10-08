import requests

from src.errors.parsing_error import ParsingError


class HHApi:
    """Реализация работы с API сайта hh.ru"""
    def __init__(self):
        self.vacancies_url = "https://api.hh.ru/vacancies"
        self.employers_url = "https://api.hh.ru/employers"
        self.__params = {
            "per_page": 100
        }

    def __get_response(self, url: str, params: dict) -> list[dict]:
        """
        Парсинг вакансий по запросу пользователя
        :param params: параметры запроса
        :return: список с информацией о вакансиях
        """
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий с сайта superjob! Статус {response.status_code}")

        return response.json()["items"]

    @staticmethod
    def __get_all_vacancies_with_ru_salary(vacancies: list[dict]) -> list[dict]:
        """
        Выбирает вакансии с зарплатой в рублях
        :param vacancies: список с информаций о вакансиях
        :return: вакансии с зарплатой в рублях
        """
        answer = []
        for res in vacancies:
            if res["salary"]["currency"] == "RUR":
                answer.append(res)

        return answer

    @staticmethod
    def put_vacancy_to_format_dict(item: dict) -> dict:
        """
        Преобразует информацию о вакансии в словарь с нужными полями
        :param item: словарь с информацией о вакансии
        :return: объект вакансии с нужными полями
        """
        min_salary = int(item["salary"]["from"]) if item["salary"]["from"] is not None else None
        max_salary = int(item["salary"]["to"]) if item["salary"]["to"] is not None else None
        new_vacancy = {
            'position': item.get("name"),
            'min_salary': min_salary,
            'max_salary': max_salary,
            'requirements': item.get("snippet").get("requirement"),
            'url': item.get("url")
        }

        return new_vacancy

    @staticmethod
    def put_employer_to_format_dict(item: dict) -> dict:
        """
        Преобразует информацию о компании в словарь с нужными полями
        :param item: словарь с информацией о компании
        :return: объект компании с нужными полями
        """
        new_vacancy = {
            'id': item.get("id"),
            'name': item.get("name"),
            'url': item.get("url")
        }

        return new_vacancy

    def get_vacancies_by_company(self, employer_id: str) -> list[dict]:
        """
        Ответ на запрос пользователя
        :param employer_id: id компании-работодателя
        :return: список вакансий компании
        """
        params = {key: value for key, value in self.__params.items()}
        params['employer_id'] = employer_id
        params["only_with_salary"] = True
        response = self.__get_response(self.vacancies_url, params)

        answer = self.__get_all_vacancies_with_ru_salary(response)
        answer = list(map(self.put_vacancy_to_format_dict, answer))

        return answer

    def get_employer_by_name(self, employer_name: str) -> list[dict]:
        """
        Получает информацию о компании по ее названию
        :param employer_name: название компании
        :return: информация по нужной компании
        """
        params = {key: value for key, value in self.__params.items()}
        params['text'] = employer_name

        response = self.__get_response(self.employers_url, params)
        return list(map(self.put_employer_to_format_dict, response))
