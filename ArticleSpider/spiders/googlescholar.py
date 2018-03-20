import scrapy
from scrapy import Request
from scrapy.selector import Selector

# from scrapy import log
from items import WanfangItem


class GoogleScholarSpider(scrapy.Spider):
    name = 'googlescholar'
    allowed_domains = ["scholar.google.com"]
    start_urls = [
        'https://scholar.google.com/scholar?start=530&q=%E5%BF%83%E8%A1%80%E7%AE%A1&hl=zh-CN&as_sdt=0,5&as_ylo=2014'

    ]

    cookies = {}

    headers = {
        # 'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
        #'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20',
        #'User-Agent': 'user-agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',

    }

    meta = {
        'dont_redirect': True,
        'handle_httpstatus_list': [301, 302]
    }


    def parse(self, response):
        for quote in response.xpath('//*[@class="gs_r gs_or gs_scl"]'):
        #for quote in response.xpath('//*[@id="gs_res_ccl_mid"]'):
            yield {
                #'title' : quote.xpath('div[2]/div[2]/h3/a').extract_first()
                #//*[@id="gs_res_ccl_mid"]/div[3]/div/h3/a
                'title' : ''.join(quote.xpath('.//h3/a//text()').extract()),
                'url' : ''.join(quote.xpath('.//h3/a//@href').extract()),
                'authors' : ''.join(quote.xpath('.//*[@class="gs_a"]//text()').extract()).split("-")[0],
                'abstract' : ''.join(quote.xpath('.//*[@class="gs_rs"]/text()').extract()),
                'cited' : ''.join(quote.xpath('.//*[@class="gs_fl"]/a[3]/text()').extract()).split("：")[-1],
                'source' : ''.join(quote.xpath('.//*[@class="gs_a"]//text()').extract()).split("-")[-1],
                'year' : ''.join(quote.xpath('.//*[@class="gs_a"]//text()').extract()).split("-")[1].split(",")[-1].replace(' ',''),
                'publish' : (','+''.join(quote.xpath('.//*[@class="gs_a"]//text()').extract()).split("-")[1]).split(",")[-2].replace(' ',''),
            }
        next_page_url = response.xpath('//*[@id="gs_n"]//td[@align="left"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
