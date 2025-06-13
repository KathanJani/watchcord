import scrapy
import os
from multiprocessing import Process, Queue
from scrapy import Selector
from urllib.parse import urlencode


def get_scrapeops_url(url):
    payload = {'api_key': os.getenv("SCRAPEOPS_API_KEY"), 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

class FlipkartSpider(scrapy.Spider):
    name = "flipkart"
    # allowed_domains = ["flipkart.com"]
    # start_urls = ["https://flipkart.com"]
    data = {'titles': [], 'mrps': [], 'discount_percentages': [], 'current_prices': [], 'images': [], 'fsns': [], 'categories': [], 'descriptions': [], 'ratings': [], 'domains': []}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

    def __init__(self, start_urls_demo: list[str]):
        super().__init__(self.name, start_urls=start_urls_demo)

    def start_requests(self):
        # urls = [
        # ]
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)
            # yield scrapy.Request(url=get_scrapeops_url(url), callback=self.parse, headers=self.headers)

    def parse(self, response):
        # if (featured_product_details_div := response.css('div.cPHDOP>div.C7fEHH').get()) is not None:
        if (featured_product_details_div := response.css('div.C7fEHH').get()) is not None:

            # Title
            if (featured_product_title_h1 := Selector(text=featured_product_details_div).css('h1._6EBuvT').get()) is not None:
                if (featured_product_title := Selector(text=featured_product_title_h1).css('span.VU-ZEz::text').get()) is not None:
                    if (featured_product_title_brand := Selector(text=featured_product_title_h1).css('span.mEh187::text').get()) is not None:
                        title = featured_product_title_brand + featured_product_title
                    else:
                        title = featured_product_title
                else:
                    title = None
            else:
                title = None

            # Check out of stock product
            if (featured_product_out_of_stock_div := response.css('div.xO1qhs div.dYhUKY>div.nyRpc8::text').get()) is None:
                # Current Price, MRP, and Discount Percentage
                if (featured_product_pricing_div := Selector(text=featured_product_details_div).css('div.x\\+7QT1>div.UOCQB1>div.hl05eU').get()) is not None:
                    if (featured_product_current_price := Selector(text=featured_product_pricing_div).css('div.Nx9bqj.CxhGGd::text').get()) is not None:
                        current_price = featured_product_current_price
                        if (featured_product_mrp := Selector(text=featured_product_pricing_div).css('div.yRaY8j.A6\\+E6v::text').getall()) is not None and (featured_product_discount := Selector(text=featured_product_pricing_div).css('div.UkUFwK.WW8yVX>span::text').get()) is not None:
                            mrp = "".join(featured_product_mrp)
                            discount_percentage = featured_product_discount
                        else:
                            mrp = current_price
                            discount_percentage = None
                    else:
                        mrp = "Product Unavailable"
                        discount_percentage = None
                        current_price = "Product Unavailable"
                else:
                    mrp = "Product Unavailable"
                    discount_percentage = None
                    current_price = "Product Unavailable"
            else:
                mrp = "Product Unavailable"
                discount_percentage = None
                current_price = "Product Unavailable"

            # Rating
            if (featured_product_rating_div := Selector(text=featured_product_details_div).css('div.ISksQ2').get()) is not None:
                if (featured_product_rating_inner_div := Selector(text=featured_product_rating_div).css('div._5OesEi.HDvrBb').get()) is not None:
                    if (featured_product_rating := Selector(text=featured_product_rating_inner_div).css('span.Y1HWO0>div.XQDdHH::text').get()) is not None:
                        rating = featured_product_rating
                    else:
                        rating = None
                else:
                    rating = None
            else:
                rating = None

        else:
            title = None
            mrp = "Product Unavailable"
            discount_percentage = None
            current_price = "Product Unavailable"
            rating = None

        # Category
        if (featured_product_category_div := response.css('div._7dPnhA').get()) is not None:
            category = []
            if (featured_product_category_divs_list := Selector(text=featured_product_category_div).css('div.r2CdBx').getall()) is not None:
                for i in range(1, len(featured_product_category_divs_list)-2):
                    category.append(featured_product_category := Selector(text=featured_product_category_divs_list[i]).css('a.R0cyWM::text').get().strip()) # type: ignore
        else:
            category = None

        # Image
        if (featured_product_img := response.css('div._4WELSP._6lpKCl>img.DByuf4.IZexXJ.jLEJ7H::attr(src)').get()) is not None:
            image = featured_product_img
        elif (featured_product_img_backup := response.css('div.gqcSqV.YGE0gZ>img._53J4C-.utBuJY::attr(src)').get()) is not None:
            image = featured_product_img_backup
        else:
            image = None

        # Description
        # if (featured_product_description_div := response.css('div.yN\\+eNk.w9jEaj').get()) is not None:
        if (featured_product_description_div := response.css('div.yN\\+eNk.w9jEaj::text').get()) is not None:
            print("LEL")
            # if (featured_product_description_p_list := Selector(text=featured_product_description_div).css('p').getall()) is not None:
            if (featured_product_description_p_list := Selector(text=featured_product_description_div).css('p::text').getall()) is not None:
                descriptions = []
                for i in range(len(featured_product_description_p_list)):
                    # descriptions.append(featured_product_description_p := Selector(text=featured_product_description_p_list[i]).css('::text').get().strip()) # type: ignore
                    descriptions.append(featured_product_description_p := featured_product_description_p_list[i].strip()) # type: ignore
                description = [' '.join(descriptions)]
            else:
                # description = [Selector(text=featured_product_description_div).css('::text').get().strip()] # type: ignore
                description = [featured_product_description_div.strip()] # type: ignore
                # description = [response.css('div.yN\\+eNk.w9jEaj::text').get().strip()] # type: ignore
        elif (featured_product_highlights_div := response.css('div.U\\+9u4y').get()) is not None:
            if (featured_product_highlights_ul := Selector(text=featured_product_highlights_div).css('div.xFVion>ul').get()) is not None:
                # if (featured_product_description_li_list := Selector(text=featured_product_highlights_ul).css('li._7eSDEz').getall()) is not None:
                if (featured_product_description_li_list := Selector(text=featured_product_highlights_ul).css('li._7eSDEz::text').getall()) is not None:
                    descriptions = []
                    for i in range(len(featured_product_description_li_list)):
                        # descriptions.append(featured_product_description_li := Selector(text=featured_product_description_li_list[i]).css('::text').get().strip()) # type: ignore
                        descriptions.append(featured_product_description_li := featured_product_description_li_list[i].strip()) # type: ignore
                    description = descriptions
                else:
                    description = None    
            else:
                description = None
        else:
            description = None

        # FSN
        fsn = response.url.split('?pid=')[1].split('&')[0]

        # Domain
        domain = response.url.split('https://')[1].split('/')[0] if 'https://' in response.url else response.url.split('http://')[1].split('/')[0]

        self.data['titles'].append(title)
        self.data['mrps'].append(mrp)
        self.data['discount_percentages'].append(discount_percentage)
        self.data['current_prices'].append(current_price)
        self.data['categories'].append(category)
        self.data['images'].append(image)
        self.data['ratings'].append(rating)
        self.data['fsns'].append(fsn)
        self.data['descriptions'].append(description)
        self.data['domains'].append(domain)
        for value in self.data.values():
            for i in range(len(value)):
                if value[i] is None:
                    value[i] = "NULL"
                else:
                    if isinstance(value[i], str):
                        value[i] = value[i].strip()
        self.log(f"Done writing {title} to dict.")
        # self.log(f"Data: {self.data}")
        # self.log(f"Raw Data: {response.text}")

    # def close(self, reason):
    #     # Check if the directory exists
    #     if not os.path.exists(directory := "demodatalol"):
    #         # Create the directory
    #         os.makedirs(directory)
    #         print(f"Directory '{directory}' created.")
    #     else:
    #         print(f"Directory '{directory}' already exists.")
    #     # Find an available file name
    #     base_filename = "demodatalol/scraped_data"
    #     file_number = 0
    #     while os.path.exists(f"{base_filename}{file_number}.csv"):
    #         file_number += 1
    #     final_filename = f"{base_filename}{file_number}.csv"

    #     # Writing the data to a CSV file using pandas
    #     # df = pd.DataFrame(self.datademo)
    #     df = pd.DataFrame(self.datademo, index=[0])
    #     df.to_csv(final_filename, index=False)

    #     self.log(f"Data written to {final_filename}.")

    # def close(self, reason):
    #     self.crawled_data = self.datademo

# Testing Stuff Here Might Delete Later
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def start_p(start_urls_demo_lol, queue):
    process = CrawlerProcess(get_project_settings())
    spider = FlipkartSpider
    process.crawl(spider, start_urls_demo=start_urls_demo_lol) #type: ignore
    process.start()
    queue.put(spider.data)

async def run_flipkart_spider(start_urls_demo):
    queue = Queue()
    try:
        process = Process(target=start_p, args=(start_urls_demo, queue))
        print(f"Process ID: {id(process)} Queue ID: {id(queue)}")
        process.start()
        result = queue.get()
        process.join()
    except Exception as e:
        print(f"Failed to run spider: {e.__class__.__name__}")
        return result
    return result

from billiard import Process as Billiard_Process #type: ignore
from billiard import Queue as Billiard_Queue #type: ignore
def run_flipkart_billiard_spider(start_urls_demo):
    queue = Billiard_Queue()
    try:
        process = Billiard_Process(target=start_p, args=(start_urls_demo, queue))
        print(f"Process ID: {id(process)} Queue ID: {id(queue)}")
        process.start()
        result = queue.get()
        process.join()
        return result
    except Exception as e:
        print(f"Failed to run spider: {e.__class__.__name__}")
        return result