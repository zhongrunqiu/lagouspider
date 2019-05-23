import scrapy
from scrapy_splash import SplashRequest
from selenium import webdriver

from ..items import LagouItem

lua_script = """
function main(splash)
    splash.images_enbled = false
    splash:go(splash.args.url)
    splash:wait(8)
    return splash:html()
end
"""

def get_cookies():
    driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    driver.get('https://www.lagou.com/')
    cookie = driver.get_cookies()
    return cookie

class LagouSpider(scrapy.Spider):
    name = 'lagouspider'
    # allow_domains = 'www.lagou.com'

    cookie = get_cookies()
    # cookie = {
    #     "JSESSIONID": "ABAAABAAAGGABCB090F51A04758BF627C5C4146A091E618",
    #     "_ga": "GA1.2.1916147411.1516780498",
    #     "_gid": "GA1.2.405028378.1516780498",
    #     "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1516780498",
    #     "user_trace_token": "20180124155458-df9f65bb-00db-11e8-88b4-525400f775ce",
    #     "LGUID": "20180124155458-df9f6ba5-00db-11e8-88b4-525400f775ce",
    #     "X_HTTP_TOKEN": "98a7e947b9cfd07b7373a2d849b3789c",
    #     "index_location_city": "%E5%85%A8%E5%9B%BD",
    #     "TG-TRACK-CODE": "index_navigation",
    #     "LGSID": "20180124175810-15b62bef-00ed-11e8-8e1a-525400f775ce",
    #     "PRE_UTM": "",
    #     "PRE_HOST": "",
    #     "PRE_SITE": "https%3A%2F%2Fwww.lagou.com%2F",
    #     "PRE_LAND": "https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2FJava%2F%3FlabelWords%3Dlabel",
    #     "_gat": "1",
    #     "SEARCH_ID": "27bbda4b75b04ff6bbb01d84b48d76c8",
    #     "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1516788742",
    #     "LGRID": "20180124181222-1160a244-00ef-11e8-a947-5254005c3644"
    # }


    start_urls = [
        'https://www.lagou.com/'
    ]
    
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0],cookies=self.cookie,callback=self.parse,)

    def parse(self,response):
        for item in response.xpath('//div[@class="menu_box"]/div/div/a'):
            job_class = item.xpath('text()').extract_first()
            job_href = item.xpath('@href').extract_first()
            job_url =job_href + '1/?filterOption=3'

            job_item = LagouItem()
            job_item['job_class'] = job_class
            job_item['job_url'] = job_url

            for i in range(1):
                job_url2 = job_href + '%s/?filterOption=3' % (i+1)
                print('*'*20,job_url2)
                yield SplashRequest(url=job_url2,
                endpoint = 'execute',
                meta={'classify_name': job_class, 'classify_href': job_href},
                dont_filter=True,
                args={'lua_source':lua_script},
                callback=self.parse_url,
                cache_args=['lua_source'])

    def parse_url(self,response):
        for sel2 in response.xpath('//ul[@class="item_con_list"]/li'):
            position_name = sel2.xpath('./div/div/div/a/h3/text()').extract()
            city = sel2.xpath('./div/div/div/a/span/em/text()').extract()
            company_name = ''.join(sel2.xpath('./div/div/div/a/text()').extract()).strip()
            salary = sel2.xpath('./div/div/div/div/span[@class="money"]/text()').extract()
            work_years = ''.join(sel2.xpath('./div/div/div/div/text()').extract()).strip()
            company_industry = ''.join(sel2.xpath('./div/div/div[@class="industry"]/text()').extract()).strip()
            desc = sel2.xpath('./div/div[@class=li_b_r]/text()').extract()


            item = LagouItem()
            item['position_name'] = position_name
            item['city'] = city
            item['company_name'] = company_name
            item['salary'] = salary
            item['work_years'] = work_years
            item['company_industry'] = company_industry
            item['desc'] = desc

            yield item
