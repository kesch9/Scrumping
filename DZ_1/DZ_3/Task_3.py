# 1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и
# реализовать функцию, записывающую собранные вакансии в созданную БД
# 2) Написать функцию, которая производит поиск и выводит на экран вакансии
# с заработной платой больше введенной суммы
# 3*)Написать функцию, которая будет добавлять в вашу базу данных
# только новые вакансии с сайта

from pymongo import MongoClient
from pprint import pprint
import pandas as pd


def add_vacancy_to_db(vac, vac_db):
    href = vac['a_href']
    res = vac_db.count_documents({'a_href': href})
    if res == 0:
        vac_db.insert_one(vac.to_dict())


def connect_db(host, port, name_db):
    client = MongoClient(host, port)
    con_db = client[name_db]
    return con_db


def find_vac_with_max_salary(sal, vac_db):
    res = vac_db.find({'max_salary': {'$gt': sal}})
    return res


def find_vac_from_site(name_site, vac_db):
    res = vac_db.find({'site': name_site})
    return res


db = connect_db('localhost', 27017, 'Task_3')
vacancy_db = db.vacancies
my_data = pd.read_csv('my.csv', index_col=0, squeeze=True)

#Заполнение БД
for vacancy in my_data.iterrows():
    add_vacancy_to_db(vacancy[1], vacancy_db)

#Поиск ЗП больше чем указанной суммы в функции(тыс.р.)
sal_max = find_vac_with_max_salary(20, vacancy_db)
for res_vac in sal_max:
    pprint(res_vac)