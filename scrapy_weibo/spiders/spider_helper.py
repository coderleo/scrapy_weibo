#coding=utf-8
import scrapy,sys,re
from scrapy import log
from scrapy.http import Request
from scrapy_weibo.items import User
class SpiderHelper():
    cookies = {
                'ALF':'1508464807',
                'SUB':'_2A250xbv3DeRhGeBO7VAQ-SrLzDmIHXVUScW_rDV6PUJbktBeLXDakW0xBMSCEelPG8xrK15fZbpO-GdyCQ..',
                'SCF':'AuPKJ83zTTyTBfaL4Qs1eohFCLiuB5k9VdKiO4y6IH0Ytuol-iukbkqXH2LvkH_I4Mp1ov6XwF2BlLcyg8VmD8w.',
                '_T_WM':'5e3852132d5295624d7bb70711b7441e',
                'SSOLoginState':'1505872807',
                'SUHB':'0bt8izEpaFWOOC',
                'SUBP':'0033WrSXqPxfM725Ws9jqgMF55529P9D9W5uyPK4nOb2dXP3Ehlq_Ip65JpX5o2p5NHD95QcehqEeK.XS0MfWs4Dqc_zi--fi-z4i-zEi--Xi-iWiKnci--ciKL2i-8si--Xi-zRi-82i--4iKnfiK.Ei--fi-2Xi-2Ni--Ni-i8iKy8i--fi-2fi-z0'
            }
    host = 'https://weibo.cn'
    max_priority = 99999
    @staticmethod
    def parse_user(rep):
        info_text = u'资料'
        u = {}
        u['user_id'] = rep.meta['user_id']
        tip = rep.xpath('//body//div[@class="u"]//div[@class="tip2"]')
        #u['nick_name'] = tip.xpath('//body//div[@class="ut"]//span[@class="ctt"]/text()').extract()[0]
        u['weibo_count'] = tip.xpath('.//span[@class="tc"]/text()').extract()[0]
        u['focus_count'] = tip.xpath('.//a/text()').extract()[0]
        u['fans_count'] = tip.xpath('.//a/text()').extract()[1]
        
        #get the url of user's information 
        url = "%s%s" %(SpiderHelper.host,rep.xpath('//body//div[@class="u"]//div[@class="ut"]//a[contains(text(),"%s")]/@href'%info_text).extract()[0])
        
        yield Request(url,callback=SpiderHelper.parse_user_further,meta=u,cookies=SpiderHelper.cookies)#,priority=(rep.meta.get('priority') or SpiderHelper.max_priority)
    @staticmethod    
    def parse_user_further(rep):
      
        u = User()
        c = rep.xpath('//body//div[@class="c"]')[2]
        info = c.xpath('.//text()')
        u['user_id'] = rep.meta['user_id']
        #u['nick_name'] = c.xpath('.//text()').extract()[0]
        for row in c.xpath('.//text()').extract():
            if u'昵称' in row:
                u['nick_name'] = row    
            if u'性别' in row:
                u['gender'] = row    
            if u'地区' in row:
                u['area'] = row    
            if u'标签' in row:
                u['labels'] = ' '.join(c.xpath('.//a//text()').extract())  
            if u'简介' in row:
                u['description'] = row        
            if u'生日' in row:
                u['birthday'] = row   
            if u'达人' in row:
                u['coolpeople'] = row
            if u'认证' in row:
                u['auth'] = row           
        #u['nick_name'] = rep.meta['nick_name']
        u['weibo_count'] = rep.meta['weibo_count']
        u['focus_count'] =rep.meta['focus_count']
        u['fans_count'] =rep.meta['fans_count']
        yield u