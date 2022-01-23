# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import re

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient



class JobparserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_base = client.vacancy

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            result_salary = self.process_salary_hh(item.get('salary'))
        elif spider.name == 'SuperJob':
            result_salary = self.process_salary_sj(item.get('salary'))
        else:
            result_salary = 123

        item['salary_min'] = result_salary[0]
        item['salary_max'] = result_salary[1]
        item['currency'] = result_salary[2]
        del item['salary']
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item

    def process_salary_hh(self, salary):
        if len(salary) > 1 and len(salary) == 5:
            salary_min = int(salary[1].replace('\xa0', u''))
            salary_max = None
            salary_currency = salary[3]
            return [salary_min, salary_max, salary_currency]
        elif len(salary) > 1 and len(salary) == 7:
            salary_min = int(salary[1].replace('\xa0', u''))
            salary_max = int(salary[3].replace('\xa0', u''))
            salary_currency = salary[5]
            return [salary_min, salary_max, salary_currency]
        else:
            salary_min = None
            salary_max = None
            salary_currency = None
            return [salary_min, salary_max, salary_currency]

    def process_salary_sj(self, salary):
        salary_temp = []
        for i in salary:
            salary_temp.append(i.replace('\xa0', u''))
        print(salary_temp)

        if len(salary) == 1:
            salary_min = None
            salary_max = None
            salary_currency = None
            return [salary_min, salary_max, salary_currency]

        if 'от' in salary_temp:
            salary_min = int(re.sub('\D', '', salary_temp[2]))
            salary_max = None
            salary_currency = re.sub('\d', '', salary_temp[2])
            return [salary_min, salary_max, salary_currency]

        if 'до' in salary_temp:
            salary_min = None
            salary_max = int(re.sub('\D', '', salary_temp[2]))
            salary_currency = re.sub('\d', '', salary_temp[2])
            return [salary_min, salary_max, salary_currency]

        if len(salary) == 4:
            salary_min = int(salary_temp[0])
            salary_max = int(salary_temp[1])
            salary_currency = salary_temp[3]
            return [salary_min, salary_max, salary_currency]
        else:
            salary_min = int(salary_temp[0])
            salary_max = None
            salary_currency = salary_temp[2]
            return [salary_min, salary_max, salary_currency]












