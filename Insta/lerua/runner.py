from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from spiders.avitoru import AvitoruSpider
from spiders.Leruaru import LeruaruSpider
from spiders.InstaCom import InstacomSpider
from lerua import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    #process.crawl(AvitoruSpider, search='щенки')
    #process.crawl(LeruaruSpider, search='stulya-dlya-kuhni')
    process.crawl(InstacomSpider, users_list= ['mark_253', 'test_1890'])
    process.start()