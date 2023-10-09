from src.db_manager.db_manager import DBManager

db = DBManager('jobs')
print(db.get_companies_and_vacancies_count())
