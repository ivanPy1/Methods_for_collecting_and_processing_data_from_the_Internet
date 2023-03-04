import scrapy
from itemloaders.processors import MapCompose, Compose, TakeFirst


# преобразование цены в int

def clean_price(value):
    try:
        value = value[0].replace(' ', '')
        value = int(value)
    except:
        return value
    return value

class LeroymerlinGoodsItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(input_processor=Compose(clean_name), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(clean_price), output_processor=TakeFirst())
    photos = scrapy.Field()
