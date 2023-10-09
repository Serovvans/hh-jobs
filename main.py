from src.db_manager.db_manager import DBManager


def example(db: DBManager):
    print("\nКомпании и количество их вакансий")
    print(db.get_companies_and_vacancies_count())
    print("\nСписок всех вакансий")
    print(db.get_all_vacancies())
    print("\nСредняя зарплата по всем вакансиям")
    print(db.get_avg_salary())
    print("\nСписок вакансий с зарплатой выше среднего значения")
    print(db.get_vacancies_with_higher_salary())
    print("\nСписок вакансий по ключевому слову")
    print(db.get_vacancies_with_keyword('программист'))


if __name__ == "__main__":
    db = DBManager('jobs')
    example(db)
