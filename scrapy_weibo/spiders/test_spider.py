#coding=utf-8
import scrapy,sys
from scrapy import log
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy_weibo.items import Post,User
reload(sys)
sys.setdefaultencoding('utf8')
class WeiboSpider(scrapy.Spider):
    page_size = 3
    name = 'test'
    allowed_domains = ['weibo.cn']
    start_urls = ['https://weibo.cn/baogeepool']
   
    def parse(self,rep):

        forward_text = u"转发"        
        comment_text = u"评论" 
        thumb_text = u"赞"
        base_fct_xpath = './/a[contains(text(),"%s")]/text()'
     
        for bindex, body in enumerate(rep.xpath("//body")):
            for dindex,div in enumerate(body.xpath('.//div[contains(@id,"M_") and @class="c"]')):
                p = Post()
                p['content'] =div.xpath('.//span[@class="ctt"]').xpath('string(.)').extract()[0]# ''.join()
                p['comment_count'] = ''.join(div.xpath(base_fct_xpath %comment_text).extract())
                p['repost_count'] = ''.join(div.xpath(base_fct_xpath %forward_text).extract())
                p['thumb_count'] = ''.join(div.xpath(base_fct_xpath %thumb_text).extract())
                p['user'] = ''.join(div.xpath('.//a[@class="nk"]/@href').extract())
                yield p
                
    def start_requests(self):
       
        for url in self.start_urls:           
           
            yield Request(url,cookies={
                'ALF':'1507286052',
                'SUB':'_2A250q790DeRhGeBO7VAQ-SrLzDmIHXVUV8E8rDV6PUJbktBeLRnikW2au912mtJG2wkfpvaHEWNbp_kd_w..',
                'SCF':'AuPKJ83zTTyTBfaL4Qs1eohFCLiuB5k9VdKiO4y6IH0YOGDVHzA89m65fLIOIZprPegRM4WCBvc5nlRCcmj6Rl4.',
                '_T_WM':'5e3852132d5295624d7bb70711b7441e',
                'SSOLoginState':'1504694052',
                'SUHB':'0vJI8mvgHPvdVz',
                'SUBP':'0033WrSXqPxfM725Ws9jqgMF55529P9D9W5uyPK4nOb2dXP3Ehlq_Ip65JpX5o2p5NHD95QcehqEeK.XS0MfWs4Dqc_\
                zi--fi-z4i-zEi--Xi-iWiKnci--ciKL2i-8si--Xi-zRi-82i--4iKnfiK.Ei--fi-2Xi-2Ni--Ni-i8iKy8i--fi-2fi-z0'
            })