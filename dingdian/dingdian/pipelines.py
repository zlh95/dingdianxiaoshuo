# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import  pymongo
from dingdian.items import DingdianItem
class MONGOPipeline(object):

    collection_name = 'dingdianxiaoshuo'

    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        '''
        cls代表这个类，因此，以下是用给定的参数创建了一个cls类的实例spider。
        参数会经过__init__方法，因为实例需要初始化。
        :param crawler: 通过crawler我们可以拿到全局配置的每个配置信息
        :return:类对象（实例）
        '''
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item,DingdianItem):
            self.db[self.collection_name].insert_one(dict(item))
            return item
