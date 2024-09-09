import scrapy


class FlipkartSpider(scrapy.Spider):
    name = "flipkart"
    allowed_domains = ["flipkart.com"]
    start_urls = ["https://flipkart.com"]

    def parse(self, response):
        pass
