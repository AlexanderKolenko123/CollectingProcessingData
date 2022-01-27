from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from spiders.avitoru import AvitoruSpider
from spiders.Leruaru import LeruaruSpider
from lerua import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AvitoruSpider, search='щенки')
    process.crawl(LeruaruSpider, search='stulya-dlya-kuhni')

    process.start()