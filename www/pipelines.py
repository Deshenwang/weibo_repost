# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html



# -*- coding: utf-8 -*-
import pymongo
from pymongo.errors import DuplicateKeyError
from www.items import UserItem, WeiboItem,UserRelationItem,FansItem,FollowItem,DiedaiItem
from www.settings import LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, DB_NAME


class MongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        db = client[DB_NAME]
        self.User = db["UserItem"]
        self.UserRelation = db["UserRelationItem"]
        self.Fans = db["FansItem"]
        self.Follow = db["FollowItem"]
        self.Diedai = db["duleisi"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, UserItem):
            self.insert_item(self.User,item)
        if isinstance(item, UserRelationItem):
            self.insert_item(self.UserRelation,item)
        if isinstance(item, FansItem):
            self.insert_item(self.Fans, item)
        if isinstance(item, FollowItem):
            self.insert_item(self.Follow,item)
        if isinstance(item, DiedaiItem):
            self.insert_item(self.Diedai,item)
        else:
            print("是什么原因呢只存一条数据")
        return item

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert(dict(item))
        except DuplicateKeyError:
            """
            说明有重复数据
            """
            pass
