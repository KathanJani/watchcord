import billiard.process
import billiard.queues
import scrapy
from pathlib import Path
import pandas as pd
import os
from multiprocessing import Process, Queue
from scrapy import Selector
from urllib.parse import urlencode
# from crochet import setup
# setup()

def get_scrapeops_url(url):
    payload = {'api_key': os.getenv("SCRAPEOPS_API_KEY"), 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    # allowed_domains = ["amazon.in"]
    # start_urls = ["https://amazon.in"]
    # data = {'titles': [], 'prices': [], 'images': [], 'asins': []}
    data = {'titles': [], 'mrps': [], 'discount_percentages': [], 'current_prices': [], 'images': [], 'asins': [], 'categories': [], 'descriptions': [], 'ratings': [], 'domains': []}
    # datademo = {}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

    def __init__(self, start_urls_demo: list[str]):
        super().__init__(self.name, start_urls=start_urls_demo)

    def start_requests(self):
        # urls = [
        # "https://www.amazon.in/dp/B0D6GPD7YS?ref=cm_sw_r_cso_wa_apan_dp_QJ8V7WZEC528NZC67XEF&ref_=cm_sw_r_cso_wa_apan_dp_QJ8V7WZEC528NZC67XEF&social_share=cm_sw_r_cso_wa_apan_dp_QJ8V7WZEC528NZC67XEF&starsLeft=1&skipTwisterOG=1",
            # "https://www.amazon.in/Assassins-Creed-Origins-Standard-Ubisoft/dp/B0DCT4F8GN/ref=sr_1_3?crid=JJK5ZF58CQ4N&dib=eyJ2IjoiMSJ9.7MxAfdtHicfJG1S_2FY8Vn3Gjm4-tpay1HV2QPBg25XOPG5eIU3p7QX2-5-8vR5ubro8iDfEi52mtZ8IjVZ0HvZK3nM_XQbqX88nG73cQGnbTeQdD0ddk4Eq5P9YAPU2ep2iz3GlghD5oaDbX-YNkq0reN06yw_Vqcoc-jNMjQziRJzVDI8aPMs9duedgey-Hpe5xrTkh5HtELYxQ0j8OG54HIQY50VVZn3XPO4W5E4.4qLuW0GnLfqgT__DQcF9WmAXXIqM08CYSf2HYCxhkyg&dib_tag=se&keywords=assassin%27s+creed+origins&qid=1725841828&sprefix=assassin%27s+creed+origi%2Caps%2C339&sr=8-3",
            # "https://www.amazon.in/Assassins-Creed-Ezio-Collection-PS4/dp/B01N8REF82/ref=sr_1_4_mod_primary_new?crid=3RUPP8GU1OEKP&dib=eyJ2IjoiMSJ9.YQ_0sJbFJv9mGUKFg1gGEuy6Rj4VzeJP6kF9yNRCFPS74wbLhTH6joYJLeshXDgPdsgAv_dj0Zuv-8g39eoifU4EiyMhl92m0v9b4mKbVXQviHlQ2hgMCv7ScbesAq5dxoZ0nNrWUfuebJzVb0-QlYxFOsN7hgG6kQKxnIrudZU3E3FWzSjViSqNb99eX_SibZEBcntzp_ZHYnws6eYgnx9HqIxR1WuapA6REhTnOGfb7iSvJD6gA764Vbif6t7dUeok2ULoMldQ5YG_HcWYI6l91d-KGcuFt2uxrq6-DiU.l6X1Udg0av0f-OKg4issz4B8rVmf70ndooVJIT9b_CM&dib_tag=se&keywords=assassin%27s+creed+2&qid=1725841859&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sprefix=assassin%27s+creed+2%2Caps%2C378&sr=8-4",
            # "https://www.amazon.in/CD-Project-Red-Cyberpunk-2077/dp/B0CP8143HY/ref=sr_1_1?crid=S6SQO7PIXKQT&dib=eyJ2IjoiMSJ9.w7wA6NhWb0vBhc-Z8gFjMaSPk3TBppOZoHpYA-PUHKbzVnd41DCx1qUlJb9DJmXFTTEHfNm-_TMCLaKu28jdNG1c34M4xuLJqWy_-cMpsyxu2B9BotvyGLQQVoHpzFvfOCEflyZKM4n3wXOofuZ1Ld-IPfbQyaBXlNpfzYj1oDvMQ7fcqgh5fBoZvDiP1m4aSNKC2y5H8lOJANrm1woEqiDagy8F1xdH_keBpk2eQ1Y.K9lMtiKRGgFfm_-bVZGDXJ46n0_xn81DxQdyH0aVW_0&dib_tag=se&keywords=cyberpunk+2077&qid=1726017376&sprefix=cyberpunk%2Caps%2C500&sr=8-1",
            # "https://www.amazon.in/BRUTON-Exclusive-Trendy-Running-Shoes/dp/B0B2JLGKPT/ref=sr_1_6?crid=FI77F3HDPON6&dib=eyJ2IjoiMSJ9.56W1QqVVkflYxG_9M9WA8ijs4dS8RMLQY6nApI5DNzH2RDNDrWbGJ7MegvIRKkNXQ6oJ4O6rTM-5fCLtwTP4oBqIet0qdIiyEbeyq2wGPd4JMSTKt1fqjhR0HTA6NlmswDOt1mRQSgJmXkedTFVCXr8LKQIzwLxYNaWp0AWmYpaq4C4hd0ti9NSHRUq7Mj_SJr3hhArXaAUy3hyEfNZtXF8Ri2GapccH96bnXA0F5EnDjnobGNtaoa31lj4CnGZufm8nrglNc35Jr2iSioWqW-jVdvg_xZZnFxdSIYTn-R4.dOAwcVkx7gjR-68SnnLDBjeAx-XJ6NXXAIaj3GFOMTY&dib_tag=se&keywords=sports+shoe&qid=1726018957&sprefix=sportsshoe%2Caps%2C193&sr=8-6",
            # "https://www.amazon.in/Formal-Shirts-Shirt-Moonlit-White-Brickwall/dp/B0CYLTYJXR/ref=sr_1_2_sspa?crid=1JYNZ0RYUEC5M&dib=eyJ2IjoiMSJ9.iRnDDYWOac1QwLWjdXQsOVvpD3LQqdkbEebodhnkn2rj_7jg3qiFusMBGoqtUzq5pQgdmG5deTsF5hEaB5lRWwtYCzJ1GU8tDLGbWpqW4y5PznxBtPiTth4CufWyqMcAx5jdEY4iv0V91WxiSsE6PUVBSK2S3-KmZuFrcmCrlKIdRfqbTP3SVP7qRFPbwl358usU9UUY8xQNSQWWRFc-AR2_tQWGFe2jygP7BPrtP7jfGBuCQGGqE53OuOvHd6JSEBtUZ-mvRGq9yp9YaDDw9Xa9IbRXc34-jU2u3zfzQlg.DLcKVWN8C2LB3BiH0UndQK1d7d5mH7GBewbXzA6ti1s&dib_tag=se&keywords=formal+shirt&qid=1726018998&sprefix=formal+shir%2Caps%2C204&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1",
            # "https://www.amazon.in/PS-Signature-RoseWood-Acoustic-Strings/dp/B0CK9822R4/ref=sr_1_4_sspa?crid=3PECT1950H5DM&dib=eyJ2IjoiMSJ9.H_dE0w8OHcmESxseNpLSvyVUezViWAqXRtHIXCiWYqxctiJGcikgqXL2jfPir_fIkROc2ujx0IhICcTW16wCAT8MxpN9kX1Z5PfINzFdmsczU9SJYXuiWxELgTqzuKNQxe4UmfjuKdhJuCdqwZN_MRE9q8qUCciXiW4fVDvnWJP5lKLgg-Di56L5HR0Ugv1NfkGXCdI5QqGcQ5hg5fe0PJ4ML5wPxTXADJfxh_9mfQfsnIorgGFCaLPo9ycTj5lFD3O7oty__Xor57aW1RlHoOLD6Q-29LmFiXi7nN7kE-0.EVYl4ZmmD4Kp2Kho8vdO-s6DhSAbB_X6-yQcGN0s_pY&dib_tag=se&keywords=guitar&qid=1726019016&sprefix=guita%2Caps%2C189&sr=8-4-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1",
            # "https://www.amazon.in/Boldfit-Basketball-Professional-Indoor-Outdoor-Training/dp/B0BQMH3HK4/ref=sr_1_1_sspa?crid=1SDC2PT36LCX4&dib=eyJ2IjoiMSJ9.IwGSM_SfWC2Z055n8UfGsOlHYZ8KcEn__8gjTNRplNmoOrhjIB84y__uYvxEmqSUeOKoUy-hosOEQI0Zy3n46dRucv-TS184LYBdPrWzVjOSd7VkQ8oNiTeBCoMVfkEYu1TKJR2LxecYBzyOH9PN0hFWiOF0lYcdXMrqFWNfVxKqtAq8hIvXyURH7ylzHnnebbMA7731CA7uFzL3AulPP0_kd38EhTdMsSYhYU1TZiqLUbRxmsHrwMdOwFrx84Furzfbegp7BfhlVYfr231Lwc1mVOwLU-cP8eyGgJPVUAM.iPii7YjRF4XO4u2JnNHUDd6hrvK-7y5n1BBmQtF4Q-A&dib_tag=se&keywords=basketball&qid=1726019056&sprefix=basketbal%2Caps%2C414&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1",
            # "https://www.amazon.in/Shocknshop-Digital-Sports-Functional-315RED/dp/B099ZNZJMW/ref=sr_1_1_sspa?crid=1Z3X885LPE8VI&dib=eyJ2IjoiMSJ9.O-wDqTB8addmxtgTSeeWEQwz1bk958CFoHaJJVMs9ubmAJ0x-saObMHgPxhFJgJCmRfGJCIs9q1HKgWKBum7HAYN0EJXrmuMt3QZkUufX6d5dg_PDJYnXl83T5NiW4t9cWsVV46n7Q0f_HGEo1A0V7DaTeWQu1Ab_MZITb7JBYASYpFqS2ZVIhOujrmIW16skT298mfnOBs2QmMafwlh1_4tMtClDCCR37IfDYzEzxL9jxjIGUH1kKNMS4WP2vX23Hk8f0GqMDiYpOESXo70DMAeFVzaPCFEnepou0COPP4.1oG_42htdlyrp9c_nNeQJln-hAEwkyOur01oanFOzjY&dib_tag=se&keywords=sports+watch+for+boys&qid=1726019119&sprefix=sports+watch+%2Caps%2C802&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1",
            
            # "https://www.amazon.in/Xivip-Detachable-Compatible-Alienware-Controller/dp/B0CYZHDT2B",
            # "https://www.amazon.in/Adventures-Sherlock-Holmes-Deluxe-Hardbound/dp/9354409008/ref=sr_1_1_sspa?crid=1I7R694I6L2IH&dib=eyJ2IjoiMSJ9.s7Wx_8J01HR30YVfE0UN8AEt7M48PpGJToGgljdwCHQ0jOQDxzSX8w0gDonUPKHjprG9A5WQVsSYXtAFOYlceG8RLdWkWsSDnz56FmiWtTMaIsoKBWKj2tBLWwboZXeEf8ydhLhoN47Y_OIuThbKEu0kmhfsWSTuNLHOsdr8Zw7_FtfGyBZvCHdaW3wR1tw5uhgYgvTSxOf3W0RuPYH1xJeTwoSE8Vr2SAqRpCj0w0A.AiunVoVOc6WWF_G2NCTO025DJmasUldclSrDdlQLB8o&dib_tag=se&keywords=sherlock+holmes+books+set&qid=1726019143&sprefix=sherlock+holm%2Caps%2C353&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1",
            # "https://www.amazon.in/dp/B08N5W4NNB?ref=cm_sw_r_cso_wa_apan_dp_7NZ7S1H61A8E7N17C97M&ref_=cm_sw_r_cso_wa_apan_dp_7NZ7S1H61A8E7N17C97M&social_share=cm_sw_r_cso_wa_apan_dp_7NZ7S1H61A8E7N17C97M&starsLeft=1&skipTwisterOG=1&th=1",
            # "https://www.amazon.in/Boat-Bassheads-242-Earphones-Resistance/dp/B09FSWY5BP/ref=asc_df_B07S9S86BF/?tag=googleshopmob-21&linkCode=df0&hvadid=709979409304&hvpos=&hvnetw=g&hvrand=4631510680890706512&hvpone=&hvptwo=&hvqmt=&hvdev=m&hvdvcmdl=&hvlocint=&hvlocphy=9197679&hvtargid=pla-811840084302&psc=1&mcid=e2294e6c11b4362c89d1afea13cf383c&gad_source=1&th=1",
            # "https://www.amazon.in/Amazon-Brand-Inkast-Casual-02_True/dp/B084DN3SZG/ref=sr_1_1_sspa?dib=eyJ2IjoiMSJ9.TJhJWOOhD34Wdi29QWFCimugjcAKy-jMtyfqoITT1NkTyd_nAoVS1hxNhGmTyAsRnSn8t9WoTfGxSNuIV2zxg9EXePicXn_xCW-Y1GOkiLWS6S7JEf_jPC27b-G6eBtpGQFKxQhoxnFZsFMrCxEaqFDJCmXAyuWobIeJfbJWHeIGR8kJw8qOLz9uN0__ERkl1AFnR8ZiLSy_8YcHyguRvDqTBK5Ihb4_3Pc8UtOt7wCx8vIvSi6zJgEFGL_Wk4D9yK1iyb3YrqfPvvQ-Lhdu3YrVIspYN3NKk8lQBU8A6rI.XTgtVzRr_WgO557yBLk-8DS_5kaI1Z_8hQW12hfY3zo&dib_tag=se&keywords=shirt&qid=1729367508&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1&psc=1",
            # "https://www.amazon.in/Transformers-Enhanced-Design-Vintage-Soundwave/dp/B08X1YW3L4/ref=sr_1_9?dib=eyJ2IjoiMSJ9.NRNwkARC2N2E5gZctZcuzIIkYCwnkPaQBKt_qvOzDDubCO6YVqVJfDtDjCWwWt1v-JM4jNsWJcnYgyelhzaE-8axVCx0giSz9oqoAW4haT-3JF-rqg2-R8F1jaZ_1qt1PrRFEQDQJ0Niuo2fJ5nkimmrbxyJbQbHyfg0W-6LbLurrXITQaWupclTA3eBjcyPhbhsZuza0o-gmxyfZQ35LMvU2wOUlU_VvaAxRZpFep0-SG3F_XCYwsRsU9dFJf2iZ0FVHYDJOuCb7lUGXRozo6Hw7uJuEylUiwAVvKOE2xk.Jz-WNMNoDR5ifRSL1z3EUxhTg-SETb5wYmP7pQq5wx4&dib_tag=se&keywords=transformers+action+figures&qid=1729413610&sr=8-9",
            # "https://www.amazon.in/Dazzl-Disinfectant-Surface-Fragrance-Suitable/dp/B0D3RDLWYP?pd_rd_w=4ALPF&content-id=amzn1.sym.535e7f8e-3856-4dd3-ab3b-f05f2328b4fa&pf_rd_p=535e7f8e-3856-4dd3-ab3b-f05f2328b4fa&pf_rd_r=M8C1FNB1R1SVW67Y0VJB&pd_rd_wg=O28xQ&pd_rd_r=a011a7fb-47c7-4ef2-bbc2-1e21e99c0fbb&pd_rd_i=B0D3RDLWYP&ref_=pd_hp_d_btf_unk_B0D3RDLWYP&th=1",
            # "https://www.amazon.in/dp/B0D2N7W1GB/ref=syn_sd_onsite_desktop_0?ie=UTF8&psc=1&pf_rd_p=fd82b077-06f6-479f-8fb9-11c7d326b43b&pf_rd_r=766N7B62V2KN867K0AG6&pd_rd_wg=iHjOW&pd_rd_w=0xrBr&pd_rd_r=70b46310-a449-4a39-826b-1159181aa2c5&aref=Uh06lSLqF4",
            # "https://www.amazon.in/MagicBook-i5-13420H-Anti-Glare-Keyboard-Fingerprint/dp/B0CXLWXYB1/ref=sr_1_1_sspa?dib=eyJ2IjoiMSJ9.MRd60dKA8Kt0qkW_Qpv-3MtbiDqmcT7jNHuG2eHu_NhtihdtT1VXW20VCcbsXwHL4kf5fpmq-jARJV-4Iw9IsI9SokqAP4wFVtvgpYMByUGevgpoqND_KBvJd5zY8vUwaXSN2BCWdEpyKJGA4aJ-iC6NfP6bGR3p4I9X7nojvIs4Rck46sueTS_w0R_Z3BxM0BfxQ22EwJKWBYB6mIGnvUK2PrDBWaNrs6rWKDQtb04.-ueF61CKANFkbgCJxzRlOvIGbl0oZsz9bXd1AVKjNRs&dib_tag=se&keywords=laptop&qid=1729367612&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1",

            # "https://www.amazon.in/John-Jacobs-Gunmetal-Rectangular-Sunglasses/dp/B0CJ5HZSR5/ref=sr_1_2_sspa?crid=YLZBK8NCKOEM&dib=eyJ2IjoiMSJ9.zhhVycchWu_G76_42bOl7osFVLC3Q0piP22jPepqbvWoD7ptaeHRJSsrxIhhFw_ZADZcGSCOrHscGa1F0er4MwSDbNj483EWoVObzcUPbG0LP-KSFsBT94vGD_zmN2QtHZD3UfJoCQjKf9EzjMG2T2MzHhJAGC3dP6Com9KqFjWdwszJmE9J7rLxrJaft6Dibkt3bPGzzPT2B-Q-PgmmMXJbTdExWPBLsa5Ll-CYeQtK-nFr94bCCQ4iFM338WhkOpqey7VOm8zAZjLRuxGRW1Pk2l8j5sIfuK9hWDvNoUo.YBfTokI1WW0XyPG7DRMM3BbKZnMj15553jUBSu3GVLM&dib_tag=se&keywords=men+sunglasses&qid=1726019192&s=apparel&sprefix=men+sunglass%2Capparel%2C307&sr=1-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"
        # ]
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)
            # yield scrapy.Request(url=get_scrapeops_url(url), callback=self.parse, headers=self.headers)

    def parse(self, response):
        # title = response.css('span#productTitle::text').get().strip()
        # pricesymbol = response.css('span.a-price-symbol::text').get()
        # price= response.css('span.a-price-whole::text').get()
        # image = response.css('img#landingImage::attr(src)').get()
        # asin = response.url.split('/dp/')[1].split('/')[0]
        # category = response.css('ul.a-unordered-list.a-nostyle.a-vertical.a-spacing-none.detail-bullet-list').get()
        # print("PRINTING:\n")
        # print("Title:", title, "Price:", pricesymbol+price, "Image:", image)

        if (title_feature_div := response.css('div#title_feature_div').get()) is not None:
            # title = response.css('div#title_feature_div>div#titleSection>h1#title>span#productTitle::text').get()
            title = Selector(text=title_feature_div).css('div#titleSection>h1#title>span#productTitle::text').get()
        else:
            title = response.css('div#titleblock_feature_div>div.a-section>h1#title>span#productTitle::text').get()

        if (corePriceDisplay_feature_div := response.css('div#corePriceDisplay_desktop_feature_div').get()) is not None:
            # pricesymbol = response.css('div#corePriceDisplay_desktop_feature_div span.priceToPay span.a-price-symbol::text').get()
            pricesymbol = Selector(text=corePriceDisplay_feature_div).css('span.priceToPay span.a-price-symbol::text').get()
            # mrp = response.css('div#corePriceDisplay_desktop_feature_div span.basisPrice>span.a-text-price>span.a-offscreen::text').get()
            mrp = Selector(text=corePriceDisplay_feature_div).css('span.basisPrice>span.a-text-price>span.a-offscreen::text').get()
            # discount_percentage = response.css('div#corePriceDisplay_desktop_feature_div span.savingsPercentage::text').get()
            discount_percentage = Selector(text=corePriceDisplay_feature_div).css('span.savingsPercentage::text').get()
            # current_price = response.css('div#corePriceDisplay_desktop_feature_div span.priceToPay span.a-price-whole::text').get()
            current_price = Selector(text=corePriceDisplay_feature_div).css('span.priceToPay span.a-price-whole::text').get()
        else:
            pricesymbol = None
            mrp = response.css('div#availability_feature_div>div#availability span.a-size-medium::text').get()
            discount_percentage = None
            # current_price = response.css('div#availability_feature_div>div#availability span.a-size-medium::text').get()
            current_price = mrp

        # if response.css('div#detailBulletsWrapper_feature_div>ul.detail-bullet-list>li span.a-text-bold::text').get() is not None and response.css('div#detailBulletsWrapper_feature_div>ul.detail-bullet-list>li span.a-text-bold::text').get() == "Best Sellers Rank:":
        if (detailBulletsWrapper_feature_div := response.css('div#detailBulletsWrapper_feature_div').get()) is not None:
            # if (detail_bullet_lists := response.css('div#detailBulletsWrapper_feature_div>ul.detail-bullet-list').getall()) is not None:
            if (detail_bullet_lists := Selector(text=detailBulletsWrapper_feature_div).css('ul.detail-bullet-list').getall()) is not None:
                for i in range(len(detail_bullet_lists)):
                    if Selector(text=detail_bullet_lists[i]).css('li>span.a-list-item>span.a-text-bold::text').get().strip() == "Best Sellers Rank:": #type: ignore
                        category = []
                        category.append(''.join(part.strip() for part in Selector(text=detail_bullet_lists[i]).css('li>span.a-list-item::text').getall()).strip().split(' in ')[1].split('(')[0].strip())
                        # category.append(''.join(part.strip() for part in response.css('div#detailBulletsWrapper_feature_div>ul.detail-bullet-list>li>span.a-list-item::text').getall()).strip().split(' in ')[1].split('(')[0].strip())
                        if Selector(text=detail_bullet_lists[i]).css('li>span.a-list-item>ul').get() is not None:
                        # if response.css('div#detailBulletsWrapper_feature_div>ul.detail-bullet-list>li>span.a-list-item>ul').get() is not None:
                            for secondary_category in Selector(text=detail_bullet_lists[i]).css('li>span.a-list-item>ul>li>span.a-list-item>a::text').getall():
                            # for secondary_category in response.css('div#detailBulletsWrapper_feature_div>ul.detail-bullet-list>li>span.a-list-item>ul>li>span.a-list-item>a::text').getall():
                                category.append(secondary_category.strip())
                        break
                    else:
                        # category = Selector(text=detail_bullet_lists[i]).css('li>span.a-list-item>span.a-text-bold::text').get()
                        category = None
            else:
                category = None
        else:
            # if response.css('div#productDetails_detailBullets_sections1>tbody>tr>th.prodDetSectionEntry::text').get() is not None and response.css('div#productDetails_detailBullets_sections1>tbody>th.prodDetSectionEntry::text').get() == "Best Sellers Rank:":
            # if (technical_product_category_section_header := response.css('div#productDetails_db_sections table#productDetails_detailBullets_sections1>tbody>tr>th.prodDetSectionEntry::text').get()) is not None and technical_product_category_section_header == "Best Sellers Rank:":
            if (productDetails_db_sections := response.css('div#productDetails_db_sections').get()) is not None:
                if (productDetails_detailBullets_sections := Selector(text=productDetails_db_sections).css('table#productDetails_detailBullets_sections1').get()) is not None:
                    # print('haha:',Selector(text=productDetails_detailBullets_sections).css('tbody').get())
                    if (productDetails_detailBullets_trs := Selector(text=productDetails_detailBullets_sections).css('tr').getall()) is not None:
                        for i in range(len(productDetails_detailBullets_trs)):
                            if Selector(text=productDetails_detailBullets_trs[i]).css('th.prodDetSectionEntry::text').get().strip() == "Best Sellers Rank": #type: ignore
                                category = []
                                for category_part in Selector(text=productDetails_detailBullets_trs[i]).css('td>span>span').getall():
                                    stripped_category = Selector(text=category_part).css('a::text').get().strip() #type: ignore
                                    category.append(stripped_category.split(' in ')[1].strip() if ' in ' in stripped_category else stripped_category.strip()) #type: ignore
                                break
                            else:
                                category = None    
                    else:
                        category = None               
                else:
                    category = None
            # category = response.css('table#productDetails_detailBullets_sections1>tbody>tr>td>span>span::text').get()
            else:
                category = None
        # category = response.css('div#detailBulletsWrapper_feature_div>ul.detail-bullet-list>li span.a-text-bold::text').get()

        image = response.css('img#landingImage::attr(src)').get()

        if (featurebullets_feature_div := response.css('div#featurebullets_feature_div').get()) is not None:
            if (feature_bullets := Selector(text=featurebullets_feature_div).css('div#feature-bullets').get()) is not None:
                if (description_ul := Selector(text=feature_bullets).css('ul.a-unordered-list.a-vertical').get()) is not None:
                    description = []
                    for description_point in Selector(text=description_ul).css('li').getall():
                        description.append(Selector(text=description_point).css('span.a-list-item::text').get().strip()) #type: ignore
                else:
                    if (productDescription_feature_div := response.css('div#productDescription_feature_div.a-row.feature').get()) is not None:
                        if (productDescription := Selector(text=productDescription_feature_div).css('div#productDescription').get()) is not None:
                            description = []
                            description.append(Selector(text=productDescription).css('p>span::text').get().strip()) #type: ignore
                        else:
                            description = None
                    else:
                        description = None
            else:
                description = None
        elif (productFactsDesktop_feature_div := response.css('div#productFactsDesktop_feature_div').get()) is not None:
            if (productFactsDesktopExpander := Selector(text=productFactsDesktop_feature_div).css('div#productFactsDesktopExpander').get()) is not None:
                if (productDescription_expander_content := Selector(text=productFactsDesktopExpander).css('div.a-expander-content').get()) is not None:
                    description = []
                    for description_ul in Selector(text=productDescription_expander_content).css('ul.a-unordered-list.a-vertical').getall():
                        description.append(Selector(text=description_ul).css('span>li>span.a-list-item::text').get().strip()) #type: ignore
                else:
                    description = None
            else:
                description = None
        elif (bookDescription_feature_div := response.css('div#bookDescription_feature_div').get()) is not None:
            if (bookDescription_expander_container := Selector(text=bookDescription_feature_div).css('div.a-expander-container').get()) is not None:
                if (bookDescription_expander_content := Selector(text=bookDescription_expander_container).css('div.a-expander-content').get()) is not None:
                    description = []
                    description.append(Selector(text=bookDescription_expander_content).css('span:first-child::text').get().strip()) #type: ignore
                    if (bookDescription_bullets := Selector(text=bookDescription_expander_content).css('ul.a-unordered-list.a-vertical').get()) is not None:
                        for bookDescription_point in Selector(text=bookDescription_bullets).css('li').getall():
                            description.append(Selector(text=bookDescription_point).css('span.a-list-item>span::text').get().strip()) #type: ignore
                    else:
                        description = None
                else:
                    description = None
            else:
                description = None
        elif (productDescription_feature_div := response.css('div#productDescription_feature_div.a-row.feature').get()) is not None:
            if (productDescription := Selector(text=productDescription_feature_div).css('div#productDescription').get()) is not None:
                description = []
                description.append(Selector(text=productDescription).css('p>span::text').get().strip()) #type: ignore
            else:
                description = None
        else:
            if (editorialReviews_feature_div := response.css('div#editorialReviews_feature_div').get()) is not None:
                if (bookDescription_section := Selector(text=editorialReviews_feature_div).css('div.a-section.a-spacing-small.a-padding-base>div.a-section.a-spacing-small.a-padding-base').get()) is not None:
                    description = []
                    description.append(Selector(text=bookDescription_section).css('span::text').get().strip()) #type: ignore
                else:
                    description = None
            else:
                description = None

        # if response.css('div#detailBullets_averageCustomerReviews span#acrPopover>span.a-declarative>a>span::text').get() is not None:
        #     rating = response.css('div#detailBullets_averageCustomerReviews span#acrPopover>span.a-declarative>a>span::text').get()
        # else:
        #     rating = response.css('div#averageCustomerReviews span#acrPopover>span.a-declarative>a>span::text').get()
        # rating = response.css('div#detailBullets_averageCustomerReviews span#acrPopover>span.a-declarative>a>span::text').get() if response.css('div#detailBullets_averageCustomerReviews span#acrPopover>span.a-declarative>a>span::text').get() is not None else response.css('div#averageCustomerReviews span#acrPopover span.a-declarative>a>span::text').get()
        rating = response.css('div#averageCustomerReviews_feature_div>div#averageCustomerReviews span#acrPopover>span.a-declarative>a>span.a-size-base::text').get()

        if len(normal_asin_link_format:= response.url.split('/dp/')[1].split('/')[0]) == 10:
            asin = normal_asin_link_format
        else:
            asin = response.url.split('/dp/')[1].split('/')[0].split('?')[0]
        # asin = response.url.split('/dp/')[1].split('/')[0] if len(response.url.split('/dp/')[1].split('/')[0]) == 10 else response.url.split('/dp/')[1].split('/')[0].split('?')[0]

        domain = response.url.split('https://')[1].split('/')[0] if 'https://' in response.url else response.url.split('http://')[1].split('/')[0]


        self.data['titles'].append(title)
        self.data['mrps'].append(mrp)
        self.data['discount_percentages'].append(discount_percentage)
        self.data['current_prices'].append(pricesymbol+current_price) if pricesymbol is not None else self.data['current_prices'].append(current_price) #type: ignore
        self.data['categories'].append(category)
        self.data['images'].append(image)
        self.data['ratings'].append(rating)
        self.data['asins'].append(asin)
        self.data['descriptions'].append(description)
        self.data['domains'].append(domain)
        # self.datademo['title'] = title
        # self.datademo['price'] = pricesymbol+price
        # self.datademo['image'] = image
        # self.datademo['asin'] = asin
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


# # Sample Code DELETE LATER
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# async def run_spider(start_urls_demo):
#     try:
#         process = CrawlerProcess(get_project_settings())
#         spider = AmazonSpider
#         process.crawl(spider, start_urls_demo=start_urls_demo) #type: ignore
#         process.start(stop_after_crawl=False)
#     except Exception as e:
#         print(f"Failed to run spider: {e.__class__.__name__}")
#         return spider.datademo
#     return spider.datademo

# Testing Stuff Here Might Delete Later
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def start_p(start_urls_demo_lol, queue):
    process = CrawlerProcess(get_project_settings())
    spider = AmazonSpider
    process.crawl(spider, start_urls_demo=start_urls_demo_lol) #type: ignore
    process.start()
    queue.put(spider.data)

async def run_spider(start_urls_demo):
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

from billiard import Process as Process2 #type: ignore
from billiard import Queue as Queue2 #type: ignore
def run_spider2(start_urls_demo):
    queue = Queue2()
    try:
        process = Process2(target=start_p, args=(start_urls_demo, queue))
        print(f"Process ID: {id(process)} Queue ID: {id(queue)}")
        process.start()
        result = queue.get()
        process.join()
        return result
    except Exception as e:
        print(f"Failed to run spider: {e.__class__.__name__}")
        return result