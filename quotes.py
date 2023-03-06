import scrapy
from scrapy.http import HtmlResponse
from quotes_toscrape_com.items import QuotesToscrapeComItem
from scrapy.loader import ItemLoader

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com"]


    def start_requests(self):
        login_link = 'http://quotes.toscrape.com/login'
        login = 'test'
        pwd = 'test'
        yield scrapy.FormRequest(login_link,
                           formdata={'username': login,
                                     'password': pwd},
                           callback=self.login)

    def login(self, response:HtmlResponse):
        quotes = response.xpath("//div[@class='quote']/span[2]/a[1]/@href").getall()
        quotes_link_photo = response.xpath("//div[@class='quote']/span[2]/a[2]/@href").getall()

        for quote in quotes:
            yield response.follow(quote, callback=self.quotes_parse)

        for quote_link in quotes_link_photo:
            yield response.follow(quote_link, callback=self.perse_photo)

    def perse_photo(self, response:HtmlResponse):
        loader = ItemLoader(item=QuotesToscrapeComItem(), response=response)
        loader.add_xpath('photos', "//div[contains(@class, 'leftContainer authorLeftContainer')]/a/img/@src")
        yield loader.load_item()

    def quotes_parse(self, response:HtmlResponse):
        author = response.xpath("//h3/text()").get()
        date_born = response.xpath("//span[@class='author-born-date']/text()").get()
        description = response.xpath("//div[@class='author-description']/text()").get()
        author_page = response.url

        yield QuotesToscrapeComItem(
            author=author,
            date_born=date_born,
            description=description,
            author_page=author_page
        )