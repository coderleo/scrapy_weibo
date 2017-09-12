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
    user = scrapy.Field()
    content = scrapy.Field()
    thumb_count = scrapy.Field()
    repost_count = scrapy.Field()
    comment_count = scrapy.Field()

class User(scrapy.Item):
    nick_name = scrapy.Field()
   
    weibo_count = scrapy.Field()
    focus_count = scrapy.Field()
    fans_count = scrapy.Field()
