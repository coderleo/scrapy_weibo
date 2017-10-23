# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyWeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class Post(scrapy.Item):
    id = scrapy.Field()
    user_id = scrapy.Field()
    content = scrapy.Field()
    thumb_count = scrapy.Field()
    repost_count = scrapy.Field()
    comment_count = scrapy.Field()
    keyword_id = scrapy.Field()
    platform = scrapy.Field()
    created_time = scrapy.Field()
class User(scrapy.Item):
    user_id = scrapy.Field()
    nick_name = scrapy.Field()
   
    weibo_count = scrapy.Field()
    focus_count = scrapy.Field()
    fans_count = scrapy.Field()
    gender = scrapy.Field()
    area = scrapy.Field()
    labels = scrapy.Field()
    birthday = scrapy.Field()
    description = scrapy.Field()
    coolpeople = scrapy.Field()
    auth = scrapy.Field()

class Forward(scrapy.Item):
    post_id = scrapy.Field()
    content = scrapy.Field()
    created_time =scrapy.Field()
    platform = scrapy.Field()
    user_id = scrapy.Field()
    parent_id = scrapy.Field()
class Comment(scrapy.Item):
    post_id = scrapy.Field()
    content = scrapy.Field()
    created_time =scrapy.Field()
    platform = scrapy.Field()
    user_id = scrapy.Field()