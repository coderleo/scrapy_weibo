#coding=utf-8
import scrapy,sys
from scrapy import log
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy_weibo.items import Post,User,Forward,Comment
reload(sys)
sys.setdefaultencoding('utf8')
class WeiboSpider(scrapy.Spider):
    host = 'https://weibo.cn'
    page_size = 2
    name = 'weibo'
    allowed_domains = ['weibo.cn']
    start_urls = []
    base_url = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%s&page=%s'
    cookies={
                'ALF':'1508049394',
                'SUB':'_2A250vwSkDeRhGeBO7VAQ-SrLzDmIHXVUQ6zsrDV6PUNbktBeLVjMkW1L2nOwxliD9kwt9l2dNZcLikNgVg..',
                'SCF':'AuPKJ83zTTyTBfaL4Qs1eohFCLiuB5k9VdKiO4y6IH0YMOjd0l3C0iBwSliEXmolUsrwSP5kEcB61Dl3QgDzsF4.',
                '_T_WM':'5e3852132d5295624d7bb70711b7441e',
                'SSOLoginState':'1505457396',
                'SUHB':'0M2FYZKN2DUfwv',
                'SUBP':'0033WrSXqPxfM725Ws9jqgMF55529P9D9W5uyPK4nOb2dXP3Ehlq_Ip65JpX5KMhUgL.Foq7Sozp1KBNS0-2dJLoIXnLxK-LBo.LBozLxKBLB.2L1hqLxKqL1-BLB-qLxKBLBonLB-BLxK.L1h-L1KzLxK-LBKBLBKMLxKMLB.-L12-LxK-LBK-LBoet'
            }
  
    def parse(self,rep):#response

        forward_text = u"转发"        
        comment_text = u"评论" 
        thumb_text = u"赞"
        
        base_fct_xpath = './/a[contains(text(),"%s")]/text()'
     
        for  body in rep.xpath("//body"):
            for div in body.xpath('.//div[contains(@id,"M_") and @class="c"]'):
                url =  div.xpath('.//a[@class="nk"]/@href').extract()[0]
                comment_url = div.xpath('.//a[contains(text(),"%s")]/@href'%comment_text).extract()[0]
                p = Post()
                p['id'] = comment_url.split('/')[-1].split('?')[0]
                p['content'] =div.xpath('.//span[@class="ctt"]').xpath('string(.)').extract()[0]# ''.join()
                p['comment_count'] = ''.join(div.xpath(base_fct_xpath %comment_text).extract())
                p['repost_count'] = ''.join(div.xpath(base_fct_xpath %forward_text).extract())
                p['thumb_count'] = ''.join(div.xpath(base_fct_xpath %thumb_text).extract())
                p['user_id'] =url.split('/')[-1]
                
                yield p
                #get users
                yield Request(url,callback=self.parse_user,cookies=self.cookies,meta={'user_id': p['user_id'] })
                #get forwards
                yield Request(comment_url,callback=self.parse_comment,cookies=self.cookies,meta={'post_id': p['id'],'comment_url':comment_url })
    def parse_comment(self,rep):        
        pages = rep.xpath('//body//input[@name="mp"]//@value').extract()
        if len(pages)>0:
            page_size = pages[0]         
            for i in xrange(int(page_size),0,-1):
                comment_url = rep.meta['comment_url'].split('#')[0]+'&page='+str(i)
                yield Request(comment_url,callback=self.parse_comment_by_page,cookies=self.cookies,meta={'post_id': rep.meta['post_id']})
        else:
            for div in rep.xpath('//body//div[contains(@id,"C_") and @class="c"]'):
                c = Comment()
                c['content'] = div.xpath('.//span[@class="ctt"]//text()').extract()[0]
                c['platform'] = div.xpath('.//span[@class="ct"]//text()').extract()[0]
                c['post_id'] = rep.meta['post_id']
                yield c
    def parse_comment_by_page(self,rep):
        for div in rep.xpath('//body//div[contains(@id,"C_") and @class="c"]'):
            c = Comment()
            c['content'] = div.xpath('.//span[@class="ctt"]//text()').extract()[0]
            c['platform'] = div.xpath('.//span[@class="ct"]//text()').extract()[0]
            c['post_id'] = rep.meta['post_id']
            yield c
    def parse_user(self,rep):
        info_text = u'资料'
        u = {}
        u['user_id'] = rep.meta['user_id']
        tip = rep.xpath('//body//div[@class="u"]//div[@class="tip2"]')
        #u['nick_name'] = tip.xpath('//body//div[@class="ut"]//span[@class="ctt"]/text()').extract()[0]
        u['weibo_count'] = tip.xpath('.//span[@class="tc"]/text()').extract()[0]
        u['focus_count'] = tip.xpath('.//a/text()').extract()[0]
        u['fans_count'] = tip.xpath('.//a/text()').extract()[1]
        
        #get the url of user's information 
        url = "%s%s" %(self.host,rep.xpath('//body//div[@class="u"]//div[@class="ut"]//a[contains(text(),"%s")]/@href'%info_text).extract()[0])
        
        yield Request(url,callback=self.parse_user_further,cookies=self.cookies,meta=u)
        
    def parse_user_further(self,rep):
      
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
        

    def start_requests(self):
        keyword = 'note8'
        for page in xrange(1,self.page_size):
            self.start_urls.append(self.base_url %(keyword,page))
        
        for url in self.start_urls:           
           
            yield Request(url,cookies=self.cookies)
