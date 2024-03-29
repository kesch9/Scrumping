# Ваше задание:
# Взять авито Авто. Собирать с использованием ItemLoader следующие данные:
#
# Название
# Все фото
# параметры Авто
# С использованием output_processor и input_processor реализовать очистку и преобразование данных.
# Значения цен должны быть в виде числового значения.
#
# Дополнительно:
# Перевести всех пауков сбора данных о вакансиях на ItemLoader и привести к единой структуре.

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from avitoparser.spiders.avito import AvitoSpider
from avitoparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AvitoSpider)
    process.start()
