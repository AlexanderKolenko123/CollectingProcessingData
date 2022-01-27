import scrapy
from itemloaders import ItemLoader
from scrapy.http import HtmlResponse
from lerua.items import LeruaParcerItem
from scrapy.loader import ItemLoader
from scrapy.selector import Selector

class LeruaruSpider(scrapy.Spider):
    name = 'Leruaru'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru']

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.start_urls = [f'https://leroymerlin.ru/catalogue/{kwargs.get("search")}']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-qa='product-name']/@href")
        for link in links:
            print(link)
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaParcerItem(), response=response)
        #name = response.xpath("//h1[@slot='title']/text()").get()
        #price = response.xpath("//span[@slot='price']/text()").get()
        #photos = response.xpath("//img[@slot='thumbs']/@src")
        #url = response.url

        loader.add_xpath('name', '//h1[@slot="title"]/text()')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpath('photos', "//img[@slot='thumbs']/@src")
        loader.add_value('url', response.url)
        yield loader.load_item()