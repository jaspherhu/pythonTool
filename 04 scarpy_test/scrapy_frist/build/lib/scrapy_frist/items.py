# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

#spider爬取后生成的数据,需要这儿用户来定义如何解析
class ScrapyFristItem(scrapy.Item):
    # define the fields for your item here like:
    #课程名字
    name = scrapy.Field()
    #课程url
    url = scrapy.Field()
    #课程url
    intruduction = scrapy.Field()
    #课程url
    pic = scrapy.Field()
    pass
