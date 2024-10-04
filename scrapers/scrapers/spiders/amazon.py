import scrapy
from pathlib import Path
import pandas as pd
import os
# from crochet import setup
# setup()

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    # allowed_domains = ["amazon.in"]
    # start_urls = ["https://amazon.in"]
    # data = {'titles': [], 'prices': [], 'images': [], 'asin': []}
    datademo = {}

    def __init__(self, start_urls_demo: list[str]):
        super().__init__(self.name, start_urls=start_urls_demo)

    def start_requests(self):
        # urls = [
        #     "https://www.amazon.in/Assassins-Creed-Origins-Standard-Ubisoft/dp/B0DCT4F8GN/ref=sr_1_3?crid=JJK5ZF58CQ4N&dib=eyJ2IjoiMSJ9.7MxAfdtHicfJG1S_2FY8Vn3Gjm4-tpay1HV2QPBg25XOPG5eIU3p7QX2-5-8vR5ubro8iDfEi52mtZ8IjVZ0HvZK3nM_XQbqX88nG73cQGnbTeQdD0ddk4Eq5P9YAPU2ep2iz3GlghD5oaDbX-YNkq0reN06yw_Vqcoc-jNMjQziRJzVDI8aPMs9duedgey-Hpe5xrTkh5HtELYxQ0j8OG54HIQY50VVZn3XPO4W5E4.4qLuW0GnLfqgT__DQcF9WmAXXIqM08CYSf2HYCxhkyg&dib_tag=se&keywords=assassin%27s+creed+origins&qid=1725841828&sprefix=assassin%27s+creed+origi%2Caps%2C339&sr=8-3",
        #     "https://www.amazon.in/Assassins-Creed-Ezio-Collection-PS4/dp/B01N8REF82/ref=sr_1_4_mod_primary_new?crid=3RUPP8GU1OEKP&dib=eyJ2IjoiMSJ9.YQ_0sJbFJv9mGUKFg1gGEuy6Rj4VzeJP6kF9yNRCFPS74wbLhTH6joYJLeshXDgPdsgAv_dj0Zuv-8g39eoifU4EiyMhl92m0v9b4mKbVXQviHlQ2hgMCv7ScbesAq5dxoZ0nNrWUfuebJzVb0-QlYxFOsN7hgG6kQKxnIrudZU3E3FWzSjViSqNb99eX_SibZEBcntzp_ZHYnws6eYgnx9HqIxR1WuapA6REhTnOGfb7iSvJD6gA764Vbif6t7dUeok2ULoMldQ5YG_HcWYI6l91d-KGcuFt2uxrq6-DiU.l6X1Udg0av0f-OKg4issz4B8rVmf70ndooVJIT9b_CM&dib_tag=se&keywords=assassin%27s+creed+2&qid=1725841859&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sprefix=assassin%27s+creed+2%2Caps%2C378&sr=8-4",
        #     "https://www.amazon.in/CD-Project-Red-Cyberpunk-2077/dp/B0CP8143HY/ref=sr_1_1?crid=S6SQO7PIXKQT&dib=eyJ2IjoiMSJ9.w7wA6NhWb0vBhc-Z8gFjMaSPk3TBppOZoHpYA-PUHKbzVnd41DCx1qUlJb9DJmXFTTEHfNm-_TMCLaKu28jdNG1c34M4xuLJqWy_-cMpsyxu2B9BotvyGLQQVoHpzFvfOCEflyZKM4n3wXOofuZ1Ld-IPfbQyaBXlNpfzYj1oDvMQ7fcqgh5fBoZvDiP1m4aSNKC2y5H8lOJANrm1woEqiDagy8F1xdH_keBpk2eQ1Y.K9lMtiKRGgFfm_-bVZGDXJ46n0_xn81DxQdyH0aVW_0&dib_tag=se&keywords=cyberpunk+2077&qid=1726017376&sprefix=cyberpunk%2Caps%2C500&sr=8-1",
        #     "https://www.amazon.in/BRUTON-Exclusive-Trendy-Running-Shoes/dp/B0B2JLGKPT/ref=sr_1_6?crid=FI77F3HDPON6&dib=eyJ2IjoiMSJ9.56W1QqVVkflYxG_9M9WA8ijs4dS8RMLQY6nApI5DNzH2RDNDrWbGJ7MegvIRKkNXQ6oJ4O6rTM-5fCLtwTP4oBqIet0qdIiyEbeyq2wGPd4JMSTKt1fqjhR0HTA6NlmswDOt1mRQSgJmXkedTFVCXr8LKQIzwLxYNaWp0AWmYpaq4C4hd0ti9NSHRUq7Mj_SJr3hhArXaAUy3hyEfNZtXF8Ri2GapccH96bnXA0F5EnDjnobGNtaoa31lj4CnGZufm8nrglNc35Jr2iSioWqW-jVdvg_xZZnFxdSIYTn-R4.dOAwcVkx7gjR-68SnnLDBjeAx-XJ6NXXAIaj3GFOMTY&dib_tag=se&keywords=sports+shoe&qid=1726018957&sprefix=sportsshoe%2Caps%2C193&sr=8-6",
        #     "https://www.amazon.in/Formal-Shirts-Shirt-Moonlit-White-Brickwall/dp/B0CYLTYJXR/ref=sr_1_2_sspa?crid=1JYNZ0RYUEC5M&dib=eyJ2IjoiMSJ9.iRnDDYWOac1QwLWjdXQsOVvpD3LQqdkbEebodhnkn2rj_7jg3qiFusMBGoqtUzq5pQgdmG5deTsF5hEaB5lRWwtYCzJ1GU8tDLGbWpqW4y5PznxBtPiTth4CufWyqMcAx5jdEY4iv0V91WxiSsE6PUVBSK2S3-KmZuFrcmCrlKIdRfqbTP3SVP7qRFPbwl358usU9UUY8xQNSQWWRFc-AR2_tQWGFe2jygP7BPrtP7jfGBuCQGGqE53OuOvHd6JSEBtUZ-mvRGq9yp9YaDDw9Xa9IbRXc34-jU2u3zfzQlg.DLcKVWN8C2LB3BiH0UndQK1d7d5mH7GBewbXzA6ti1s&dib_tag=se&keywords=formal+shirt&qid=1726018998&sprefix=formal+shir%2Caps%2C204&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1",
        #     "https://www.amazon.in/PS-Signature-RoseWood-Acoustic-Strings/dp/B0CK9822R4/ref=sr_1_4_sspa?crid=3PECT1950H5DM&dib=eyJ2IjoiMSJ9.H_dE0w8OHcmESxseNpLSvyVUezViWAqXRtHIXCiWYqxctiJGcikgqXL2jfPir_fIkROc2ujx0IhICcTW16wCAT8MxpN9kX1Z5PfINzFdmsczU9SJYXuiWxELgTqzuKNQxe4UmfjuKdhJuCdqwZN_MRE9q8qUCciXiW4fVDvnWJP5lKLgg-Di56L5HR0Ugv1NfkGXCdI5QqGcQ5hg5fe0PJ4ML5wPxTXADJfxh_9mfQfsnIorgGFCaLPo9ycTj5lFD3O7oty__Xor57aW1RlHoOLD6Q-29LmFiXi7nN7kE-0.EVYl4ZmmD4Kp2Kho8vdO-s6DhSAbB_X6-yQcGN0s_pY&dib_tag=se&keywords=guitar&qid=1726019016&sprefix=guita%2Caps%2C189&sr=8-4-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1",
        #     "https://www.amazon.in/Boldfit-Basketball-Professional-Indoor-Outdoor-Training/dp/B0BQMH3HK4/ref=sr_1_1_sspa?crid=1SDC2PT36LCX4&dib=eyJ2IjoiMSJ9.IwGSM_SfWC2Z055n8UfGsOlHYZ8KcEn__8gjTNRplNmoOrhjIB84y__uYvxEmqSUeOKoUy-hosOEQI0Zy3n46dRucv-TS184LYBdPrWzVjOSd7VkQ8oNiTeBCoMVfkEYu1TKJR2LxecYBzyOH9PN0hFWiOF0lYcdXMrqFWNfVxKqtAq8hIvXyURH7ylzHnnebbMA7731CA7uFzL3AulPP0_kd38EhTdMsSYhYU1TZiqLUbRxmsHrwMdOwFrx84Furzfbegp7BfhlVYfr231Lwc1mVOwLU-cP8eyGgJPVUAM.iPii7YjRF4XO4u2JnNHUDd6hrvK-7y5n1BBmQtF4Q-A&dib_tag=se&keywords=basketball&qid=1726019056&sprefix=basketbal%2Caps%2C414&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1",
        #     "https://www.amazon.in/Shocknshop-Digital-Sports-Functional-315RED/dp/B099ZNZJMW/ref=sr_1_1_sspa?crid=1Z3X885LPE8VI&dib=eyJ2IjoiMSJ9.O-wDqTB8addmxtgTSeeWEQwz1bk958CFoHaJJVMs9ubmAJ0x-saObMHgPxhFJgJCmRfGJCIs9q1HKgWKBum7HAYN0EJXrmuMt3QZkUufX6d5dg_PDJYnXl83T5NiW4t9cWsVV46n7Q0f_HGEo1A0V7DaTeWQu1Ab_MZITb7JBYASYpFqS2ZVIhOujrmIW16skT298mfnOBs2QmMafwlh1_4tMtClDCCR37IfDYzEzxL9jxjIGUH1kKNMS4WP2vX23Hk8f0GqMDiYpOESXo70DMAeFVzaPCFEnepou0COPP4.1oG_42htdlyrp9c_nNeQJln-hAEwkyOur01oanFOzjY&dib_tag=se&keywords=sports+watch+for+boys&qid=1726019119&sprefix=sports+watch+%2Caps%2C802&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1",
        #     "https://www.amazon.in/Adventures-Sherlock-Holmes-Deluxe-Hardbound/dp/9354409008/ref=sr_1_1_sspa?crid=1I7R694I6L2IH&dib=eyJ2IjoiMSJ9.s7Wx_8J01HR30YVfE0UN8AEt7M48PpGJToGgljdwCHQ0jOQDxzSX8w0gDonUPKHjprG9A5WQVsSYXtAFOYlceG8RLdWkWsSDnz56FmiWtTMaIsoKBWKj2tBLWwboZXeEf8ydhLhoN47Y_OIuThbKEu0kmhfsWSTuNLHOsdr8Zw7_FtfGyBZvCHdaW3wR1tw5uhgYgvTSxOf3W0RuPYH1xJeTwoSE8Vr2SAqRpCj0w0A.AiunVoVOc6WWF_G2NCTO025DJmasUldclSrDdlQLB8o&dib_tag=se&keywords=sherlock+holmes+books+set&qid=1726019143&sprefix=sherlock+holm%2Caps%2C353&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1",
        #     "https://www.amazon.in/John-Jacobs-Gunmetal-Rectangular-Sunglasses/dp/B0CJ5HZSR5/ref=sr_1_2_sspa?crid=YLZBK8NCKOEM&dib=eyJ2IjoiMSJ9.zhhVycchWu_G76_42bOl7osFVLC3Q0piP22jPepqbvWoD7ptaeHRJSsrxIhhFw_ZADZcGSCOrHscGa1F0er4MwSDbNj483EWoVObzcUPbG0LP-KSFsBT94vGD_zmN2QtHZD3UfJoCQjKf9EzjMG2T2MzHhJAGC3dP6Com9KqFjWdwszJmE9J7rLxrJaft6Dibkt3bPGzzPT2B-Q-PgmmMXJbTdExWPBLsa5Ll-CYeQtK-nFr94bCCQ4iFM338WhkOpqey7VOm8zAZjLRuxGRW1Pk2l8j5sIfuK9hWDvNoUo.YBfTokI1WW0XyPG7DRMM3BbKZnMj15553jUBSu3GVLM&dib_tag=se&keywords=men+sunglasses&qid=1726019192&s=apparel&sprefix=men+sunglass%2Capparel%2C307&sr=1-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"

        # ]
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.css('span#productTitle::text').get().strip()
        pricesymbol = response.css('span.a-price-symbol::text').get()
        price= response.css('span.a-price-whole::text').get()
        image = response.css('img#landingImage::attr(src)').get()
        asin = response.url.split('/dp/')[1].split('/')[0]
        # category = response.css('ul.a-unordered-list.a-nostyle.a-vertical.a-spacing-none.detail-bullet-list').get()
        # print("PRINTING:\n")
        # print("Title:", title, "Price:", pricesymbol+price, "Image:", image)
        # self.datademo['title'].append(title)
        # self.datademo['price'].append(pricesymbol+price)
        # self.datademo['image'].append(image)
        # self.datademo['asin'].append(asin)
        self.datademo['title'] = title
        self.datademo['price'] = pricesymbol+price
        self.datademo['image'] = image
        self.datademo['asin'] = asin
        self.log(f"Done writing {title} to dict.")

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
    #     df = pd.DataFrame(self.data)
    #     df.to_csv(final_filename, index=False)

    #     self.log(f"Data written to {final_filename}.")

    # def close(self, reason):
    #     self.crawled_data = self.datademo


# Sample Code DELETE LATER
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
async def run_spider(start_urls_demo):
    try:
        process = CrawlerProcess(get_project_settings())
        spider = AmazonSpider
        process.crawl(spider, start_urls_demo=start_urls_demo) #type: ignore
        process.start()
    except Exception as e:
        print(f"Failed to run spider: {e.__class__.__name__}")
        return spider.datademo
    return spider.datademo