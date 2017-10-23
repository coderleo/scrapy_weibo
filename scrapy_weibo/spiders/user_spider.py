#coding=utf-8
import scrapy,sys,re,urllib
from scrapy import log
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy_weibo.items import Post
from spider_helper import SpiderHelper
from ..db_config import MySQLConfig
from ..sql_helper import SqlHelper
from ..time_helper import format_time
from ..redis_helper import RedisHelper
reload(sys)
sys.setdefaultencoding('utf8')
class Userpider(scrapy.Spider):
    name = 'user'
    allowed_domains = ['weibo.cn']
    start_urls = []
    base_url = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%s&page=%s'
    page_size = 2
    redis_db = RedisHelper()
    def start_requests(self):
      
        for url in self.redis_db.pop():  
            print url           
            yield Request(url,callback=SpiderHelper.parse_user,meta={'user_id': url.split('/')[-1]},cookies=SpiderHelper.cookies)
 