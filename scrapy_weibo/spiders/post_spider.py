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
class PostSpider(scrapy.Spider):
    name = 'post'
    allowed_domains = ['weibo.cn']
    start_urls = []
    base_url = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%s&page=%s'
    page_size = 2
    redis_db = RedisHelper()
    def start_requests(self):
        
        #keyword = 'note8'
        db = SqlHelper(MySQLConfig)
        for keyword in db.select_keyword():             
            for page in xrange(1,self.page_size):
                self.start_urls.append((self.base_url %(keyword[1],page),keyword[0]))
        print '**********************************'+str(len(self.start_urls))
        for url in self.start_urls:
            
            yield Request(url[0],cookies=SpiderHelper.cookies,meta={'keyword_id':url[1]},priority=99999)
       
    def parse(self,rep):#response

        forward_text = u"转发"        
        comment_text = u"评论" 
        thumb_text = u"赞"
        pa = re.compile(r'\d+')
        base_fct_xpath = './/div[last()]//a[contains(text(),"%s")]/%s'
        base_fct_text = 'text()'
        base_fct_href = '@href'
        for  body in rep.xpath("//body"):
            for div in body.xpath('.//div[contains(@id,"M_") and @class="c"]'):
                url =  div.xpath('.//a[@class="nk"]/@href').extract()[0]
                #print base_fct_xpath %(base_fct_href,comment_text)
                comment_url = div.xpath(base_fct_xpath %(comment_text,base_fct_href)).extract()[0]
                forward_url = div.xpath(base_fct_xpath %(forward_text,base_fct_href)).extract()[0]
                p = Post()
                p['id'] = comment_url.split('/')[-1].split('?')[0]
                p['content'] =div.xpath('.//span[@class="ctt"]').xpath('string(.)').extract()[0]# ''.join()
                p['comment_count'] = int(pa.findall(''.join(div.xpath(base_fct_xpath %(comment_text,base_fct_text)).extract()))[0])
                p['repost_count'] =  int(pa.findall(''.join(div.xpath(base_fct_xpath  %(forward_text,base_fct_text)).extract()))[0])
                p['thumb_count'] =  int(pa.findall(''.join(div.xpath(base_fct_xpath %(thumb_text,base_fct_text)).extract()))[0])
                p['user_id'] =url.split('/')[-1]
                p['keyword_id'] =rep.meta['keyword_id']
                ct = div.xpath('.//span[@class="ct"]/text()').extract()[0].split(u'来自')
                if len(ct)>1:
                    p['platform'] =ct[1]
                #print format_time(ct[0])
                p['created_time'] =ct[0]
                yield p
                self.redis_db.push(url)
                #get users
                #yield Request(url,callback=SpiderHelper.parse_user,meta={'user_id': p['user_id']},cookies=SpiderHelper.cookies)
               
