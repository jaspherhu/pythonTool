# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import json
import pymongo
import sqlite3
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

#保存json文件
class ScrapyFristPipeline:
    def open_spider(self, spider):    
        self.file = open('items.jl', 'w')
 
    def close_spider(self, spider):
        self.file.close()
 
    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(line)   #.decode('gb2312').encode('utf-8')
        return item
    
# 保存csv
class ScrapySecondPipeline:
    def __init__(self):
        headers = ('name', 'url', 'intruduction', 'pic')
        self.f = open('mv_kk52.csv', 'w+', encoding='utf-8', newline='')
        self.f_csv = csv.DictWriter(self.f, headers)
        self.f_csv.writeheader()  # 写入表头

    def process_item(self, item, spider):
        self.f_csv.writerow(item)
        return item

    def close_spider(self, spider):
        self.f.close()
        print('mv_kk52.csv文件写入完成')

#保存mango文件
class ScrapyThridPipeline(object):
    #collection_name = 'url_runoob'  #表单名字(二级)
    #collection_name = 'url_KK52'  #表单名字(二级)
    collection_name = 'url_kk52_dh2'  #表单名字(二级)

    def __init__(self, mongo_url, mongo_port, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url,self.mongo_port)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        self.db[self.collection_name].update_one({'url_token': item['url_token']}, {'$set': dict(item)}, True)

        #print('echo item value:',item)
        #if item['url_token']:
            #self.db[self.collection_name].update_one({'url_token':item['url_token']},{'$set':item},True)

        return item

name = "chbill_bill_msg"
path_db = '/gitee/py_tool/10_django/mysite/charg.sqlite3'
#不知道为啥不能使用{}来插入字符 name到 CREATE TABLE IF NOT EXISTS blog_bill_msg和INSERT INTO blog_bill_msg
#保存mysqlite文件
class ScrapySqlitePipeline(object):
    #def __init__(self, sqlite_file, sqlite_table):
    def __init__(self, sqlite_file, sqlite_name):
        self.sqlite_file = sqlite_file      #db名字
        self.table_name = sqlite_name
 
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_file=crawler.settings.get('SQLITE_DB'),  # 从 settings.py 提取
            sqlite_name=crawler.settings.get('SQLITE_TABLE_NAME')
        )
 
    def open_spider(self, spider):
        self.conn = sqlite3.connect(path_db)
        #self.conn = sqlite3.connect(self.sqlite_file)
        self.cur = self.conn.cursor() #self.conn.cursor
        #引号越多,可以写入的行数就越多

        query = """
        CREATE TABLE IF NOT EXISTS chbill_bill_msg (
            id  INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT DEFAULT  '0',
            url TEXT DEFAULT  '0',
            intruduction TEXT DEFAULT  '0',
            pic TEXT DEFAULT  '0',
            up_time TEXT DEFAULT  '0'
        );
        """
        self.cur.execute(query)
        self.conn.commit()
 
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()   
    
    def process_item(self, item, spider):
        query = """
        INSERT INTO chbill_bill_msg (name, url, intruduction, pic, up_time)
        VALUES (?, ?, ?, ?, ?);
        """

        #insert_sqlite3_msg = "INSERT INTO chbill_bill_msg (name, url, introduction, pic, up_time) VALUES (%s, %s, %s, %s)",(item['name'], item['url'], item['intruduction'], item['pic'])
        self.cur.execute(query, (item['name'], item['url'], item['intruduction'], item['pic'], item['up_time']))

        #在数据库查询刚才execute这条数据
        if self.cur.fetchone() is None:
            self.conn.commit()
        else:
            print('item exists in the database.',item)
        return item