import scrapy

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

        for box in response.xpath('/html/body/div[4]/div/div[2]/div[%d]'):
            for box2 in box.xpath('/a[%d]'):
                item['name'] = box2.xpath('/h4').text
                item['url'] = box2.xpath('[@class="item-top item-1"]').text
                item['intruduction'] = box2.xpath('/strong').text
                item['pic'] = box2.xpath('\img').text
        
        #for box in range(1,10):
            #item['name'] = "hufan"
            #item['url'] = "https://www.runoob.com"
            #item['intruduction'] = "菜鸟"
            #item['pic'] = "\img"

            yield item
        #return item   
        #pass
