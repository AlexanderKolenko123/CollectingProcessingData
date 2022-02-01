# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import os
from pymongo import MongoClient
from urllib.parse import urlparse


class ParserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.instagram_scr

    def Add2db(self, item, collection_name):
        collection = self.mongo_base[collection_name]
        try:
            collection.insert_one(item)
        except Exception as e:
            print(e, item)
            pass

    def process_item(self, item, spider):
        self.Add2db(item, spider.name)
        return item


class PhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
        return info.spider.search + '/' + os.path.basename(urlparse(request.url).path)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    # def file_path(self, request, response=None, info=None, *, item=None):
    #     return ''
