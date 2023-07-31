# 1.Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json

url = 'https://api.github.com'
user = 'Elen2312'

response = requests.get(f'{url}/users/{user}/repos')

with open('exercise_1.json', 'w') as f:
    json.dump(response.json(), f)

for i in response.json():
    print(i['name'])

# 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое,
# требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

url = 'https://api.oilpriceapi.com/v1/prices/latest'
headers = {
    'Authorization': 'Token 60984d8869d015ef97c98bc55b9df96c',
    'Content-Type': 'application/json'
}

response = requests.get(url=url, headers=headers)

with open('exercise_2.json', 'w') as f:
    json.dump(response.json(), f)

print(response.json())
