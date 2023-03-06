from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from pymongo import MongoClient


class QuotesToscrapeComPipeline:
    def process_item(self, item, spider):
        return item

class QuotesToscrapeComPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
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
        MONGO_DATABASE = 'quotes_db'

        client = MongoClient(MONGO_URI)
        self.mongo_base = client[MONGO_DATABASE]

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item
