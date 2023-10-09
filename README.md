# hh-jobs

Модуль для работы с вакансиями интересующих компаний с сайта hh.ru

## Требования

- Python >= 3.8
- Зависимости из файла pyproject.toml

## Установка

1. Убедитесь, что у вас установлен Poetry (https://python-poetry.org/docs/#installation).
2. Клонируйте репозиторий: `git clone https://github.com/your-username/your-repo.git`
3. Перейдите в директорию проекта: `cd your-repo`
4. Установите зависимости с помощью Poetry: `poetry install`
5. Активируйте виртуальное окружение Poetry: `poetry shell`

## Как использовать
1. Запуск примера работы всех методов
Примеры использования:
```python
from main import example
from src.db_manager.db_manager import DBManager

db = DBManager('Название базы данных')
example(db)

```
2. Работа с api сайтов поиска вакансий
```python
from src.api.hh_api import HHApi

api = HHApi()
employer_id = 0 # id компании на сайте hh в формате int
vacancies = api.get_vacancies_by_company(employer_id)
employer = api.get_employer_by_id(employer_id)

```
3. Работа с базой данных
```python
from src.db_manager.db_manager import DBManager

db = DBManager('Название базы данных')
db.get_companies_and_vacancies_count() # Вызов метода класса DBManager
```

## Структура проекта

1. src - модули и пакеты реализующие логику бота и работу с пользователем
   - api - модули для работы с различными api поиска вакансий
   - errors - кастомные классы ошибок, для обработки особенных исключений
   - db_manager - модуль для создания, заполнения и работы с базой данных
2. main.py - содержит функцию с примером работы всех методов DBManager

## Статус проекта
Завершён
