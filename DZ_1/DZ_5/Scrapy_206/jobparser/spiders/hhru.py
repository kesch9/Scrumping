# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?text=Python&area=113&st=searchVacancy']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)
        vacancy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()
        for link in vacancy:
            yield response.follow(link, self.vacancy_parse)

    def vacancy_parse (self, response: HtmlResponse):
        name = response.css('div.vacancy-title h1.header::text').extract_first()
        int_sal = get_salary(response.css('div.vacancy-title p.vacancy-salary::text').extract_first())
        href = response.url
        site = self.name
        if len(int_sal) == 2:
            salary_min = int_sal[0]
            salary_max = int_sal[1]
        else:
            salary_min = 0
            salary_max = 0
        yield JobparserItem(name=name, salary_min=salary_min, salary_max=salary_max, href=href, site=site)


def get_salary(sal):
    sal.replace('руб.', '').replace(' ', '')\
        .replace('-', ' ').replace('от', '').replace('до', ' ')
    if sal:
        return [int(s) for s in sal.split() if s.isdigit()]
    return [0, 0]
