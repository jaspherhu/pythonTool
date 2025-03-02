import scrapy
import re

#按照item那儿需要的数据,把东西解析出来送出去
from scrapy_frist.items import ScrapyFristItem

class MvKk52Spider(scrapy.Spider):
    #name = "mv_kk52"
    allowed_domains = ["www.52kkba.com"]
    start_urls = ["https://www.52kkba.com/play/plist/1.html"]

    def parse(self, response):

        #先实例化一个容器,容器的格式已经在items.py中定义好了
        item = ScrapyFristItem()
        matchs = r'["【""】"\s]'
        res = response.xpath('//ul[@class="row list-inline"]/li')
        #nxt_urls = "https://www.52kkba.com"+response.xpath('//div[contains(@style,"line")]/a[6]/@href').extract_first()
        nxt_urls = ""

        for box in res:
            name_t = box.xpath('./p[1]/a/@title').extract_first()
            item['name'] = re.sub(matchs,'',name_t)
            item['url'] = "https://www.52kkba.com"+box.xpath('./div/a/@href').extract_first()
            item['intruduction'] = box.xpath('./p[2]/text()').extract_first()
            item['pic'] = box.xpath('./div/a/img/@src').extract_first()
            item['up_time'] = 20240607
            yield item  

        res = response.xpath('//div[contains(@style,"line")]/a[@class="pagegbk"]')
        for box in res:
            gaol = box.xpath('./text()').extract_first()
            

            if (gaol == "下一页"):
                #print('hit next page:',"https://www.52kkba.com"+box.xpath('./@href').extract_first())
                nxt_urls = "https://www.52kkba.com"+box.xpath('./@href').extract_first()
                print('search next page:',nxt_urls)
                break
        
        if nxt_urls:
            yield scrapy.Request(nxt_urls, callback=self.parse,dont_filter=False)
            print('jump to the nxt page:',nxt_urls)
        else:
            print('crawl mv over:',nxt_urls)

        pass
