from pprint import pprint
from lxml import html
import requests

head = {'User-agent': 'Chrome/77.0.3865.7'}


def requests_to_mail():
    try:
        request = requests.get('https://mail.ru', headers=head)
        root = html.fromstring(request.text)
        result_list = root.xpath(
            "//div[@class='news-item__inner']//a[contains(@href, 'http')]")
        if result_list:
            for i in result_list:
                print(i.text)
        else:
            print("At your request to mail no results were found. Please, check your request.")

    except requests.exceptions.ConnectionError:
        print("No connection to site")
        exit(1)


def requests_to_lenta():
    try:
        request = requests.get('https://lenta.ru', headers=head)
        root = html.fromstring(request.text)
        result_list = root.xpath(
            "//section[contains(@class, 'box')]//div/a[contains(@href, '/news/2019')]")
        if result_list:
            for i in result_list:
                print(i.text)
        else:
            print("At your request to lenta no results were found. Please, check your request.")

    except requests.exceptions.ConnectionError:
        print("No connection to site")
        exit(1)


if __name__ == '__main__':
    requests_to_mail()
    requests_to_lenta()
