from src.api.hh_api import HHApi

api = HHApi()
employers = ['3Т - Time Table Technologies', '3ХЛ Логистика', '410Web',
                 '42 MEDIA', '3-Дизайн', '3 Step IT', '37bytes', '365 DIGITAL TECH',
                 '33 пингвина', '29 Вольт', '12VOLT']
data = dict()
for emp in employers:
    inf = api.get_employer_by_name(employer_name=emp)[0]
    data[inf['id']] = inf['name']
print(data)
