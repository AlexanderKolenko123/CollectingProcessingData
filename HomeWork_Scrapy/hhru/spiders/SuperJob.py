import scrapy
from scrapy.http import HtmlResponse
from hhru.items import JobparserItem

class SuperjobSpider(scrapy.Spider):
    allowed_domains = ['superjob.ru']
    start_urls = [
        'https://www.superjob.ru/vacancy/search/?keywords=Python developer&geo[t][0]=4',
        'https://spb.superjob.ru/vacancy/search/?keywords=Python developer']
    name = 'SuperJob'

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@class,'f-test-link-Dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[contains(@class,'icMQ_ _6AfZ9')]/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        salary = response.xpath("//span[@class='_2Wp8I _3a-0Y _3DjcL _3fXVo']/text()").getall()
        url = response.url

        yield JobparserItem(name=name, salary=salary, url=url)