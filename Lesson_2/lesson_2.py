from bs4 import BeautifulSoup
from pprint import pprint
import requests
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
params = {'page': 0}
url = 'https://hh.ru/search/vacancy'
session = requests.Session()

articles_list = []

while True:
    response = session.get(
        url + '?search_field=name&search_field=company_name&search_field=description&enable_snippets=false&text=data+scientist&',
        headers=headers, params=params)
    parsed = BeautifulSoup(response.text, 'html.parser')

    articles = parsed.find_all('div', {'class': 'serp-item'})
    if not articles:
        break
    for article in articles:
        articles_info = {}

        info = article.find('a', {'class': 'serp-item__title'})
        vacancy = info.text
        articles_info['vacancy'] = vacancy

        link = info.get('href')
        articles_info['link'] = link

        company = article.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).text
        articles_info['company'] = company

        city = article.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
        articles_info['city'] = city

        salary = article.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if not salary:
            salary_min = None
            salary_max = None
            salary_currency = None
        else:
            salary = salary.text.replace('\u202f', '').split(' ')
            if salary[0] == 'до':
                salary_min = None
                salary_max = int(salary[1])
            elif salary[0] == 'от':
                salary_min = int(salary[1])
                salary_max = None
            elif len(salary) == 1:
                salary_min = int(salary[0])
                salary_max = None
            else:
                salary_min = int(salary[0])
                salary_max = int(salary[2])
            salary_currency = salary[-1]
        articles_info['salary_min'] = salary_min
        articles_info['salary_max'] = salary_max
        articles_info['salary_currency'] = salary_currency
        articles_list.append(articles_info)
    print(f"Обработана страница №{params['page']}")
    params['page'] += 1

df = pd.DataFrame(articles_list)
pd.set_option('display.max_columns', None)
print(df[4:10])

df.to_csv('hh.csv')
