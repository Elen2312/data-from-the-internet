# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, которая будет
# добавлять только новые вакансии в вашу базу.

import json
import pymongo
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
with open('../Lesson_2/hh.json') as j_file:
    file = json.load(j_file)

db = client['vacancies']
hh = db.hh
double_vacancy = []
hh.create_index([('vacancy', pymongo.ASCENDING), ('company', pymongo.ASCENDING), ('city', pymongo.ASCENDING)],
                unique=True)
for vacancy in file:
    if '_id' in vacancy:
        del vacancy['_id']
    try:
        hh.insert_one(vacancy)
    except DuplicateKeyError:
        print(f'Such a document already exists.')
        del vacancy['_id']
        double_vacancy.append(vacancy)
with open('double.json', 'w') as double:
    json.dump(double_vacancy, double)

print(f'Number of vacancies: {hh.count_documents({})}')

# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой
# суммы (необходимо анализировать оба поля зарплаты, то есть цифра вводится одна, а запрос проверяет оба поля)

salary = input('Заработная плата больше - ')


def search_vacancies(wage):
    for doc in hh.find({'$or': [{'salary_min': {'$gt': int(wage)}},
                                {'salary_max': {'$gt': int(wage)}}
                                ]
                        }
                       ):
        pprint(doc)


search_vacancies(salary)
