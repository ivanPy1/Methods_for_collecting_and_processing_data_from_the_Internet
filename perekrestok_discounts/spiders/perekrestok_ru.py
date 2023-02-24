import scrapy

from scrapy.http import HtmlResponse
from perekrestok_discounts.items import PerekrestokDiscountsItem


class PerekrestokRuSpider(scrapy.Spider):
    name = "perekrestok_ru"

    allowed_domains = ["perekrestok.ru"]

    start_urls = ["https://www.perekrestok.ru/cat/d"]

    def parse(self, response: HtmlResponse):
        urls_product = response.xpath("//a[@class='sc-fFucqa dUNCjf product-card__link']/@href").getall()

        discounts_items = response.xpath("//div[@class='product-card-wrapper']").getall()
        name_item = response.xpath("//div[@class='catalog-content__list']/div/div/div/div/div/a/span/text()").getall()
        old_price_item = response.xpath("//div[@class='price-old']/text()").getall()
        new_price_item = response.xpath("//div[@class='price-new']/text()").getall()
        rating_item = response.xpath("//div[@class='rating-value']/text()").getall()
        link_item = urls_product


        yield PerekrestokDiscountsItem(
            name=name_item,
            old_price=old_price_item,
            new_price=new_price_item,
            rating=rating_item,
            link=link_item
        )
