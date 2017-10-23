# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json,re
import codecs
from .time_helper import format_time
from sql_helper import SqlHelper
from db_config import MySQLConfig
class ScrapyWeiboPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = codecs.open('items.jl', 'w',encoding='utf8')
        self.file_user = codecs.open('user.jl', 'w',encoding='utf8')
        self.file_forward = codecs.open('forward.jl','w',encoding='utf8')
<<<<<<< HEAD
        self.file_comment = codecs.open('comment.jl','w',encoding='utf8')
        self.sql_helper = SqlHelper(MySQLConfig)
        self.each_count = 50
        self.post_count = 0
        self.posts = []

        self.user_count = 0
        self.users = []
=======
>>>>>>> aa77b0edc1eb9cebce262ca728b7630058f1f7a1
    def process_item(self, item, spider):
        
        if 'Post' in str(item.__class__):
            item['created_time'] =format_time(item['created_time']).strftime('%Y-%m-%d %H:%M:%S')
            if self.post_count>self.each_count:   
                self.post_count = 0     

                self.sql_helper.insert_post(self.posts)
                self.posts = []
            else:
                self.posts.append([(item['id'],item['user_id'],item['content'],item['repost_count'],item['thumb_count'],\
                item['comment_count'],item['created_time'],1,item.get('platform','')),(item['id'],item['keyword_id'])])
                self.post_count = self.post_count + 1
        if 'User' in str(item.__class__):
             pa = re.compile(r'\d+')
             item['fans_count'] = int(pa.findall(item['fans_count'])[0])
             item['focus_count'] = int(pa.findall(item['focus_count'])[0])
             item['weibo_count'] = int(pa.findall(item['weibo_count'])[0])
             item['gender'] = 1 if item.get('gender','').replace(u'性别:','')==u'男' else 0
             item['auth'] = item.get('auth','').replace(u'认证信息:','')
             item['birthday'] = item.get('birthday','').replace(u'生日:','')
             item['area'] = item.get('area','').replace(u'地区:','')
             item['description'] = item.get('description','').replace(u'简介:','')
             item['nick_name'] = item['nick_name'].replace(u'昵称:','')
             item['labels'] = item.get('labels','').replace(u'更多>>','')
             if self.user_count>2:   
                self.user_count = 0     

                self.sql_helper.insert_user(self.users)
                self.users = []
             else:
                self.users.append([(item['user_id'],item.get('description',''),item['nick_name'],item['gender'],item['labels'],\
                item['auth'],item['birthday'],item['focus_count'],item['weibo_count'],item['fans_count'])])
                self.user_count = self.user_count + 1
        if 'Comment' in str(item.__class__):
            line = json.dumps(dict(item),indent=4, ensure_ascii=False) + "\n"
            self.file_forward.write(line)
        return item
