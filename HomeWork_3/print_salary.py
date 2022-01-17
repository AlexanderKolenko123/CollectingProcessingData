from pymongo import MongoClient

client = MongoClient(port=27017)
db = client.HH

# Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
def print_salary(salary):
    objects = db.hh.find({'salary_max': {'$gt': salary}})
    for obj in objects:
        print(obj)

print_salary(10000)