import re
import scrapy
import requests 
from lxml import etree
#按照item那儿需要的数据,把东西解析出来送出去
from scrapy_frist.items import ScrapyFristItem

# 设置请求头，包含token  
headers = {  
    'Content-Type': 'application/json',  # 假设服务器期望接收JSON格式的数据  
    #'Authorization': 'Bearer ' + token   # 设置Authorization头部，包含token  
    #'Cookie': '_token=eyJhbGciOiJIUzI1NiJ9.eyJfaWRfIjoiTXBKVUNPekZ2N0lKS1RjYkc0emo1dz09IiwiYXVkIjoic2luZXhjZWwiLCJpc3MiOiJzaW5leGNlbCIsImV4cCI6MTcxNzE4MTEzM30.dA8DZkkhMMNrYhxyYu4Wo2Kwe536LSXIitH6lYxH17A',  
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'  # 伪装的User-Agent  
}  

class MvKk52DhSpider(scrapy.Spider):
    name = "mv_kk52_dh"
    allowed_domains = ["www.52kkba.com"]
    start_urls = ["https://www.52kkba.com/play/rbdh.php"]

    def parse(self, response):
        #先实例化一个容器,容器的格式已经在items.py中定义好了
        item = ScrapyFristItem()
        matchs = r'["【""】"\s]'
        res = response.xpath('//div[contains(@class,"mb-2")]')
        #nxt_urls = "https://www.52kkba.com"+response.xpath('//div[contains(@style,"line")]/a[6]/@href').extract_first()
        nxt_urls = ""

        for box in res:
            name_t = box.xpath('./p/a/text()').extract_first()
            item['name'] = re.sub(matchs,'',name_t)                                             #名字
            item['url'] = "https://www.52kkba.com"+box.xpath('./div/a/@href').extract_first()   #链接
            item['intruduction'] = box.xpath('./p/font/text()').extract_first()                 #集数
            item['pic'] = box.xpath('./div/a/img/@src').extract_first()                         #图片链接
            item['up_time'] = 20240607

            #resp = requests.get(item['url'], headers=headers)  
            #resp.encoding = 'utf-8'
            #html = etree.HTML(resp.text)
            #scrapy.Request(nxt_urls, callback=self.parse,dont_filter=False)
            #item['up_time'] = html.xpath('//div[@id="nr_lt"]/p[5]/font/text()')
            #item['intruduction'] =  html.xpath('//*[@id="nr_lt"]/text()[2]')+html.xpath('//*[@id="nr_lt"]/p[6]/text()')
            
            yield item  

        res = response.xpath('//p[contains(@align,"center")]/a')
        for box in res:
            gaol = box.xpath('./text()').extract_first()

            if (gaol == "后一页"):
                nxt_urls = "https://www.52kkba.com/play/rbdh.php"+box.xpath('./@href').extract_first()
                print('search next page:',nxt_urls)
                break
        
        if nxt_urls:
            yield scrapy.Request(nxt_urls, callback=self.parse,dont_filter=False)
            print('jump to the nxt page:',nxt_urls)
        else:
            print('crawl mv over:',nxt_urls)

        pass
