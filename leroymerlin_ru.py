import scrapy
from scrapy.http import HtmlResponse
from leroymerlin_goods.items import LeroymerlinGoodsItem
from scrapy.loader import ItemLoader


class LeroyMerlinRuSpider(scrapy.Spider):
    name = 'leroymerlin_ru'

    allowed_domains = ['leroymerlin.ru']

    start_urls = ['https://leroymerlin.ru/catalogue/mezhkomnatnye-dveri/']


    def parse(self, response:HtmlResponse):
        pages_links = response.xpath("//div[@class='phytpj4_plp largeCard']/a")
        for link in pages_links:
         yield response.follow(link, callback=self.parse_goods)

    def parse_goods(self, response:HtmlResponse):
        loader = ItemLoader(item=LeroymerlinGoodsItem(), response=response)

        loader.add_xpath('name', "//div[@data-testid='product-title_mf-pdp']/div/h1/span/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('price', "//div[@data-testid='prices_mf-pdp']/showcase-price-view/span[@slot='price']/text()")
        loader.add_xpath('photos', "//picture/source/@srcset")
        yield loader.load_item()


