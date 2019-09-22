# 1) Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы)
# с сайта superjob.ru и hh.ru. Приложение должно анализировать несколько страниц сайта(также вводим через
# input или аргументы). Получившийся список должен содержать в себе минимум:
#
#     *Наименование вакансии
#     *Предлагаемую зарплату (отдельно мин. и и отдельно макс.)
#     *Ссылку на саму вакансию
#     *Сайт откуда собрана вакансия
# По своему желанию можно добавить еще работодателя и расположение. Данная структура должна быть
# одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
from pandas import DataFrame as df
import time


def get_salary(sal):
    sal.replace('руб.', '').replace(' ', '')\
        .replace('-', ' ').replace('от', '').replace('до', ' ')
    if sal:
        return [int(s) for s in sal.split() if s.isdigit()]
    return [0, 0]


head = {'User-agent': 'Chrome/77.0.3865.7'}
main_link_hh='https://spb.hh.ru'
main_link_superjob='https://www.superjob.ru'
search_hh = '/search/vacancy?L_is_autosearch=false&area=2&clusters=true&enable_snippets=true&text=Data+scientist&page='
html_hh = requests.get(main_link_hh+search_hh + '0', headers=head).text
html_super_job = requests.get(main_link_superjob+'/vacancy/search/?keywords=Data%20scientist', headers=head).text
parsed_html_hh = bs(html_hh, 'html.parser')
count_page = parsed_html_hh.findAll('a', {'data-qa': 'pager-page'})
i = int(count_page[-1].getText())-1
time.sleep(2)
min_salary = 0
max_salary = 0
vacancies_list = []
for page in range(i):
    html_hh = requests.get(main_link_hh + search_hh + str(page), headers=head).text
    parsed_html_hh = bs(html_hh, 'html.parser')
    # ('a', {'data-qa': 'vacancy-serp__vacancy-title'}):
    for vac_page in parsed_html_hh.findAll('div', {'data-qa': 'vacancy-serp__vacancy'}):
        vacancy = {}
        desc = vac_page.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        vacancy['name_vacancy'] = desc.getText()
        vacancy['a_href'] = desc['href']
        salary = vac_page.find('div', {'class': 'vacancy-serp-item__compensation'})
        if salary:
            int_sal = get_salary(salary.getText().replace('\xa0', ' '))
            if len(int_sal) == 2:
                vacancy['min_salary'] = int_sal[0]
                vacancy['max_salary'] = int_sal[1]
            else:
                vacancy['min_salary'] = min_salary
                vacancy['max_salary'] = int_sal[0]
        else:
            vacancy['min_salary'] = min_salary
            vacancy['max_salary'] = min_salary
        vacancy['site'] = 'hh.ru'
        vacancies_list.append(vacancy)
    time.sleep(2)


# SuperJOB
parsed_html_super_job = bs(html_super_job, 'html.parser')
vac_page = parsed_html_super_job.findAll('div', {'class': '_3zucV _2GPIV f-test-vacancy-item i6-sc _3VcZr'})
for vac in vac_page:
    vacancy = {}
    href = vac.find('a', {'target' : '_blank'})
    salary = vac.find('span', {'class' : '_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'})
    vacancy['name_vacancy'] = href.getText()
    vacancy['a_href'] = href['href']
    if salary:
        int_sal = get_salary(salary.getText().replace('\xa0', ' '))
        if len(int_sal) == 2:
            vacancy['min_salary'] = int_sal[0]
            vacancy['max_salary'] = int_sal[1]
        else:
            vacancy['min_salary'] = min_salary
            vacancy['max_salary'] = max_salary
    else:
        vacancy['min_salary'] = min_salary
        vacancy['max_salary'] = max_salary
    vacancy['site'] = 'superjob.ru'
    vacancies_list.append(vacancy)

pprint(vacancies_list)

myDataset = df.from_dict(vacancies_list)
myDataset.to_csv('my.csv')
# time.sleep(2)
