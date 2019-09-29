import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperJobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a[rel=next]::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)
        vacancy = response.css('a[target=_blank]::attr(href)').extract()
        print(vacancy)
        for link in vacancy[0:19]:
            yield response.follow(link, self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css('div._3MVeX h1::text').extract_first()
        int_sal = get_salary(response.css('div._3mfro').extract_first())
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
    sal.replace('руб.', '').replace(' ', '') \
        .replace('-', ' ').replace('от', '').replace('до', ' ')
    if sal:
        return [int(s) for s in sal.split() if s.isdigit()]
    return [0, 0]