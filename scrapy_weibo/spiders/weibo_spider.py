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
    name = 'weibo'
    allowed_domains = ['weibo.cn']
    start_urls = []
    base_url = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%s&page=%s'
    cookies={
                'ALF':'1507286052',
                'SUB':'_2A250q790DeRhGeBO7VAQ-SrLzDmIHXVUV8E8rDV6PUJbktBeLRnikW2au912mtJG2wkfpvaHEWNbp_kd_w..',
                'SCF':'AuPKJ83zTTyTBfaL4Qs1eohFCLiuB5k9VdKiO4y6IH0YOGDVHzA89m65fLIOIZprPegRM4WCBvc5nlRCcmj6Rl4.',
                '_T_WM':'5e3852132d5295624d7bb70711b7441e',
                'SSOLoginState':'1504694052',
                'SUHB':'0vJI8mvgHPvdVz',
                'SUBP':'0033WrSXqPxfM725Ws9jqgMF55529P9D9W5uyPK4nOb2dXP3Ehlq_Ip65JpX5o2p5NHD95QcehqEeK.XS0MfWs4Dqc_\
                zi--fi-z4i-zEi--Xi-iWiKnci--ciKL2i-8si--Xi-zRi-82i--4iKnfiK.Ei--fi-2Xi-2Ni--Ni-i8iKy8i--fi-2fi-z0'
            }
  
    def parse(self,rep):#response

        forward_text = u"转发"        
        comment_text = u"评论" 
        thumb_text = u"赞"
        base_fct_xpath = './/a[contains(text(),"%s")]/text()'
     
        for  body in rep.xpath("//body"):
            for div in body.xpath('.//div[contains(@id,"M_") and @class="c"]'):
                p = Post()
                p['content'] =div.xpath('.//span[@class="ctt"]').xpath('string(.)').extract()[0]# ''.join()
                p['comment_count'] = ''.join(div.xpath(base_fct_xpath %comment_text).extract())
                p['repost_count'] = ''.join(div.xpath(base_fct_xpath %forward_text).extract())
                p['thumb_count'] = ''.join(div.xpath(base_fct_xpath %thumb_text).extract())
                p['user'] = ''.join(div.xpath('.//a[@class="nk"]/@href').extract())
                yield p
                yield Request(p['user'],callback=self.parse_user,cookies=self.cookies)
    def parse_user(self,rep):
        u = User()
        tip = rep.xpath('//body//div[@class="u"]//div[@class="tip2"]')
        u['nick_name'] = tip.xpath('//body//div[@class="ut"]//span[@class="ctt"]/text()').extract()[0]
        u['weibo_count'] = tip.xpath('.//span[@class="tc"]/text()').extract()[0]
        u['focus_count'] = tip.xpath('.//a/text()').extract()[0]
        u['fans_count'] = tip.xpath('.//a/text()').extract()[1]
        yield u
    def start_requests(self):
        keyword = 'note8'
        for page in xrange(1,self.page_size):
            self.start_urls.append(self.base_url %(keyword,page))
        
        for url in self.start_urls:           
           
            yield Request(url,cookies=self.cookies)
