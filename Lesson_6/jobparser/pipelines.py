# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('mongodb://127.0.0.1:27017/')
        self.db = client['vacancy']

    def process_item(self, item, spider):

        salary = self.salary_parse(item['salary'])

        vacancy = item['vacancy']
        city = item['city']
        salary_min = salary[0]
        salary_max = salary[1]
        salary_currency = salary[2]
        link = item['link']

        vacancy_json = {'vacancy': vacancy,
                        'city': city,
                        'salary_min': salary_min,
                        'salary_max': salary_max,
                        'salary_currency': salary_currency,
                        'link': link}

        collection = self.db[spider.name]
        collection.insert_one(vacancy_json)
        return vacancy_json

    def salary_parse(self, salary):
        salary_min = None
        salary_max = None
        salary_currency = None

        for i in range(len(salary)):
            salary[i] = salary[i].replace(u'\xa0', u'')

        if salary[0] == 'до ':
            salary_max = salary[1]
        elif len(salary) == 6 and salary[0] == 'от ':
            salary_min = salary[1]
        elif len(salary) >= 8 and salary[1] == salary[3]:
            salary_max = salary[1]
        else:
            salary_min = salary[1]
            salary_max = salary[3]
        salary_currency = salary[-3]
        result = [salary_min,
                  salary_max,
                  salary_currency]

        return result
