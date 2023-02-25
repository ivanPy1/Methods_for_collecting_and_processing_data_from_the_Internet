import scrapy

from scrapy.http import HtmlResponse

from parser_books.items import ParserBooksItem

class LabirintRuSpider(scrapy.Spider):
    name = "labirint_ru"
    allowed_domains = ["labirint.ru"]
    start_urls = ["https://www.labirint.ru/best/sale/"]

    # next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
    # if next_page:
    #     yield response.follow(next_page, callback=self.parse)

    def parse(self, response: HtmlResponse):
        urls_books = response.xpath("//div[@class='product-cover']//a[@class='product-title-link']/@href").getall()
        for url_vacancy in urls_books:
            yield response.follow(url_vacancy, callback=self.books_parse)

    def books_parse(self, response: HtmlResponse):
        link_book = response.url
        books_title = response.xpath("//div[@class='prodtitle']/h1/text()").get()
        authors = response.xpath("//a[@data-event-label='author']/text()").get()
        basic_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        discount_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        rating = response.xpath("//div[@id='rate']/text()").get()

        yield ParserBooksItem(
            link_book=link_book,
            books_title=books_title,
            authors=authors,
            basic_price=basic_price,
            discount_price=discount_price,
            rating=rating
        )
