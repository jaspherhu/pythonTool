import scrapy
import re

#按照item那儿需要的数据,把东西解析出来送出去
from scrapy_frist.items import ScrapyFristItem

class MyspiderSpider(scrapy.Spider):
    name = "myspider"#每个spider的name,用来区分生成不同的爬虫名字
    allowed_domains = ["www.runoob.com"] #允许爬取的域名,用于过滤下面这些请求的链接
    start_urls = ["https://www.runoob.com/"]

    #承接上面爬取的数据(response),该方法负责提取数据生成item或者生成需要进一步request的数据
    def parse(self, response):
        #先实例化一个容器,容器的格式已经在items.py中定义好了
        item = ScrapyFristItem()
        matchs = r'["【""】"\s]'
        url_list = response.xpath('//a[contains(@class,"item-top")]')

        for box in url_list:
            name_t = box.xpath('./h4/text()').extract_first()
            item['name'] = re.sub(matchs,'',name_t)
            item['url'] = "http"+box.xpath('.//@href').extract_first()
            item['intruduction'] = box.xpath('.//strong/text()').extract_first()
            item['pic'] = box.xpath('.//img/@src').extract_first()

            yield item  
        pass
