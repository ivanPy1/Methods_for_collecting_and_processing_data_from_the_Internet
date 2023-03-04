from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from pymongo import MongoClient


class LeroymerlinGoodsPipeline:
    def process_item(self, item, spider):
        return item


class LeroymerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                start_url = 'https://leroymerlin.ru/'
                img = start_url + img
                try:
                    yield Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item


class MongoPipeline(object):
    def __init__(self):
        MONGO_URI = 'mongodb://localhost:27017'
        MONGO_DATABASE = 'leroy_merlin_goods_db'

        client = MongoClient(MONGO_URI)
        self.mongo_base = client[MONGO_DATABASE]

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item
