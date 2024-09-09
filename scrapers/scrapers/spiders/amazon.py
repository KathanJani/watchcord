import scrapy
from pathlib import Path

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.in"]
    # start_urls = ["https://amazon.in"]

    def start_requests(self):
        urls = [
            "https://www.amazon.in/Assassins-Creed-Origins-Standard-Ubisoft/dp/B0DCT4F8GN/ref=sr_1_3?crid=JJK5ZF58CQ4N&dib=eyJ2IjoiMSJ9.7MxAfdtHicfJG1S_2FY8Vn3Gjm4-tpay1HV2QPBg25XOPG5eIU3p7QX2-5-8vR5ubro8iDfEi52mtZ8IjVZ0HvZK3nM_XQbqX88nG73cQGnbTeQdD0ddk4Eq5P9YAPU2ep2iz3GlghD5oaDbX-YNkq0reN06yw_Vqcoc-jNMjQziRJzVDI8aPMs9duedgey-Hpe5xrTkh5HtELYxQ0j8OG54HIQY50VVZn3XPO4W5E4.4qLuW0GnLfqgT__DQcF9WmAXXIqM08CYSf2HYCxhkyg&dib_tag=se&keywords=assassin%27s+creed+origins&qid=1725841828&sprefix=assassin%27s+creed+origi%2Caps%2C339&sr=8-3",
            "https://www.amazon.in/Assassins-Creed-Ezio-Collection-PS4/dp/B01N8REF82/ref=sr_1_4_mod_primary_new?crid=3RUPP8GU1OEKP&dib=eyJ2IjoiMSJ9.YQ_0sJbFJv9mGUKFg1gGEuy6Rj4VzeJP6kF9yNRCFPS74wbLhTH6joYJLeshXDgPdsgAv_dj0Zuv-8g39eoifU4EiyMhl92m0v9b4mKbVXQviHlQ2hgMCv7ScbesAq5dxoZ0nNrWUfuebJzVb0-QlYxFOsN7hgG6kQKxnIrudZU3E3FWzSjViSqNb99eX_SibZEBcntzp_ZHYnws6eYgnx9HqIxR1WuapA6REhTnOGfb7iSvJD6gA764Vbif6t7dUeok2ULoMldQ5YG_HcWYI6l91d-KGcuFt2uxrq6-DiU.l6X1Udg0av0f-OKg4issz4B8rVmf70ndooVJIT9b_CM&dib_tag=se&keywords=assassin%27s+creed+2&qid=1725841859&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sprefix=assassin%27s+creed+2%2Caps%2C378&sr=8-4",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # custom_settings = {
    #     'FEED_FORMAT': 'csv',  # Save in CSV format
    #     'FEED_URI': 'data/products.csv',  # Path to save the CSV file
    #     'FEED_EXPORT_ENCODING': 'utf-8'  # Encoding to avoid any character issues
    # }
    def parse(self, response):
        titles = response.css('span.a-size-medium.a-color-base.a-text-normal::text').getall()
        prices = response.css('span.a-price > span.a-offscreen::text').getall()
        print(response.text)
        # for item in zip(titles, prices):
        #     print( {
        #         'title': item[0],
        #         'price': item[1]
        #     })