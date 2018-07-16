# -*- coding: utf-8 -*-
import pymongo
from douban.settings import mongo_db_name,mongo_host,mongo_port,mongo_db_collection

class DoubanPipeline(object):
    def __init__(self):
        host = mongo_host
        port = mongo_port
        dbname = mongo_db_name
        sheetname = mongo_db_collection
        client = pymongo.MongoClient(host=host,port=port)
        mydb = client[dbname]
        self.post = mydb[sheetname]
    def process_item(self, item, spider):
        # item即为传过来的数据
        data = dict(item)
        self.post.insert(data)
        return item