from pprint import pprint
import requests
from pymongo import MongoClient
from lxml import html
import time

def get_mail_news():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    news = []
    main_link = 'https://lenta.ru'
    response = requests.get(main_link)
    root = html.fromstring(response.text)
    top_news_links = root.xpath("//div[@class='topnews__column']/a/@href | //div[@class='topnews__column']/div/a/@href")
    top_new_text = root.xpath("//div[@class='topnews__column']/a/div/span/text() | //div[@class='topnews__column']/div/a/div/h3/text()")
    print(top_news_links)

    date_time = []
    for i in top_news_links:
        def_xpatf = "//time[@class='topic-header__item topic-header__time']/text()"
        if 'https' in i:
            def_xpatf = "//span[contains(@class,'time')]/text()"
            request = requests.get(i, headers=header)
        else:
            request = requests.get(main_link + i, headers=header)
        root = html.fromstring(request.text)
        date = root.xpath(def_xpatf)
        print(date)
        date_time.extend(date)

    keys = ('title', 'date', 'link')
    for item in list(zip(top_new_text, date_time, top_news_links)):
        news_dict = {}
        for key, value in zip(keys, item):
            news_dict[key] = value

        news_dict['source'] = 'lenta.ru'
        news.append(news_dict)
    return news

def add2Mongo(news):
    client = MongoClient(port=27017)
    db = client.NEWS
    for item in news:
            db.NEWS.insert_one(item)

newNews = get_mail_news()
pprint(newNews)
mg = add2Mongo(newNews)


