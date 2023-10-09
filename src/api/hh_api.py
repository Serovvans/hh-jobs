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

    @staticmethod
    def __get_response(url: str, params: dict):
        """
        Парсинг вакансий по запросу пользователя
        :param params: параметры запроса
        :return: список с информацией о вакансиях
        """
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий с сайта superjob! Статус {response.status_code}")

        return response.json()

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
        if item["salary"]["from"] is None:
            min_salary = int(item["salary"]["to"])
        else:
            min_salary = int(item["salary"]["from"])

        if item["salary"]["to"] is None:
            max_salary = min_salary
        else:
            max_salary = int(item["salary"]["to"])

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
            'id': item['id'],
            'name': item['name'],
            'url': item['alternate_url']
        }

        return new_vacancy

    def get_vacancies_by_company(self, employer_id: int) -> list[dict]:
        """
        Ответ на запрос пользователя
        :param employer_id: id компании-работодателя
        :return: список вакансий компании
        """
        params = {key: value for key, value in self.__params.items()}
        params['employer_id'] = employer_id
        params["only_with_salary"] = True
        response = self.__get_response(self.vacancies_url, params)["items"]

        answer = self.__get_all_vacancies_with_ru_salary(response)
        answer = list(map(self.put_vacancy_to_format_dict, answer))
        answer = [item for item in answer if item['position'] is not None]

        return answer

    def get_employer_by_id(self, employer_id: int) -> dict:
        """
        Получает информацию о компании по ее названию
        :param employer_id: id компании
        :return: информация по нужной компании
        """
        params = {key: value for key, value in self.__params.items()}

        response = self.__get_response(f"{self.employers_url}/{employer_id}", params)

        return self.put_employer_to_format_dict(response)
