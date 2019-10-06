# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from avitoparser.items import AvitoRealEstate
from scrapy.loader import ItemLoader

class AvitoSpider(scrapy.Spider):
    name = 'auto'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/sankt-peterburg/avtomobili?cd=1']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath('//a[@class="item-description-title-link"]/@href').extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)
        pass

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoRealEstate(), response=response)
        loader.add_xpath('photos',
                         '//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url')
        loader.add_css('title', 'h1.title-info-title span.title-info-title-text::text')
        loader.add_xpath('model', '//div[contains(@class, "item-params")]//li[1]/text()')
        loader.add_xpath('year', '//div[contains(@class, "item-params")]//li[5]/text()')
        loader.add_xpath('price', '//span[contains(@class, "js-item-price")]/@content')
        yield loader.load_item()


