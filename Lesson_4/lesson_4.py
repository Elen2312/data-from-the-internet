# 1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru,
# lenta.ru. Для парсинга использовать XPath. Структура данных должна содержать:
# - название источника;
# - наименование новости;
# - ссылку на новость;
# - дата публикации.

import requests
import json

from lxml import html
from pprint import pprint
from pymongo import MongoClient

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
response = requests.get('https://lenta.ru/', headers=headers)

dom = html.fromstring(response.text)
news = []
items = dom.xpath("//a[contains(@class,'card-mini')]")

for item in items:
    news_dict = {}
    title = item.xpath(".//h3[contains(@class,'card-mini__title')]/text()")
    link = item.xpath("./@href")
    time = item.xpath(".//time[contains(@class,'card-mini__info-item')]//text()")

    news_dict['title'] = title
    news_dict['link'] = link
    news_dict['time'] = time

    news.append(news_dict)

pprint(news)

# 2. Сложить собранные новости в БД
with open('news.json', 'w') as file:
    json.dump(news, file)

client = MongoClient('127.0.0.1', 27017)
db = client['news']
news_db = db.news

with open('news.json') as file:
    file = json.load(file)

for news in file:
    news_db.insert_one(news)

print(f'Number of news: {news_db.count_documents({})}')
