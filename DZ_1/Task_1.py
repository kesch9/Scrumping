# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.
import requests
from requests.auth import HTTPBasicAuth
import json
head = {'User-agent': 'Chrome/77.0.3865.7'}
main_link = 'https://api.github.com'
users = 'users'
orgs = 'orgs'
nick = 'kesch9'
repos = 'repos'
req = requests.get(f'{main_link}/{users}/{nick}/repos', headers=head)
with open('data.json', 'w', encoding='utf-8') as f:
    if req.ok:
        data = json.loads(req.text)
        for i in data:
            json.dump(i['name'], f, ensure_ascii=False)
# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# # Выполнить запросы к нему, пройдя авторизацию через curl, Postman, Python.
# # Ответ сервера записать в файл (приложить скриншот для Postman и curl)
req = requests.get('https://api.github.com/user', auth=HTTPBasicAuth('user', 'pass'))
print(req)