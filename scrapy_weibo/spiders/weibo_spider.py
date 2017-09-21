#coding=utf-8
import scrapy,sys,re
from scrapy import log
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy_weibo.items import Post,User,Forward,Comment
reload(sys)
sys.setdefaultencoding('utf8')
class WeiboSpider(scrapy.Spider):
    host = 'https://weibo.cn'
    page_size = 2
    max_priority = 99999
    name = 'weibo'
    allowed_domains = ['weibo.cn']
    start_urls = []
    base_url = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%s&page=%s'
    cookies={
                'ALF':'1508464807',
                'SUB':'_2A250xbv3DeRhGeBO7VAQ-SrLzDmIHXVUScW_rDV6PUJbktBeLXDakW0xBMSCEelPG8xrK15fZbpO-GdyCQ..',
                'SCF':'AuPKJ83zTTyTBfaL4Qs1eohFCLiuB5k9VdKiO4y6IH0Ytuol-iukbkqXH2LvkH_I4Mp1ov6XwF2BlLcyg8VmD8w.',
                '_T_WM':'5e3852132d5295624d7bb70711b7441e',
                'SSOLoginState':'1505872807',
                'SUHB':'0bt8izEpaFWOOC',
                'SUBP':'0033WrSXqPxfM725Ws9jqgMF55529P9D9W5uyPK4nOb2dXP3Ehlq_Ip65JpX5o2p5NHD95QcehqEeK.XS0MfWs4Dqc_zi--fi-z4i-zEi--Xi-iWiKnci--ciKL2i-8si--Xi-zRi-82i--4iKnfiK.Ei--fi-2Xi-2Ni--Ni-i8iKy8i--fi-2fi-z0'
            }
  
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
                
                yield p
                #get users
                yield Request(url,callback=self.parse_user,cookies=self.cookies,meta={'user_id': p['user_id']})
                #get forwards
                if p['repost_count'] <>0:
                    yield Request(forward_url,callback=self.parse_forward,cookies=self.cookies,meta={'post_id': p['id'],'forward_url':forward_url })
                #get comment
                if p['comment_count'] <>0:
                    yield Request(comment_url,callback=self.parse_comment,cookies=self.cookies,meta={'post_id': p['id'],'comment_url':comment_url })
    
    def parse_forward(self,rep):        
        pages = rep.xpath('//body//input[@name="mp"]//@value').extract()
        if len(pages)>0:
            page_size = pages[0]         
            for i in xrange(int(page_size),0,-1):
                forward_url = rep.meta['forward_url'].split('#')[0]+'&page='+str(i)
                
                yield Request(forward_url,callback=self.parse_forward_by_page,cookies=self.cookies,meta={'post_id': rep.meta['post_id'],'priority':i},\
                priority=i)
        else:
            for f in  self.populate_forward(rep):
                yield f
    def parse_forward_by_page(self,rep):
        for f in  self.populate_forward(rep):
            yield f
    def populate_forward(self,rep):
        for div in rep.xpath('//body//span[@class="ct"]/..'):
            urls = div.xpath('.//a//@href').extract()
            user_url =  urls[0]
            f = Forward()            
            f['content'] = div.xpath('.//text()').extract()[1]
            f['platform'] =div.xpath('.//text()[last()]').extract()[0]
            f['post_id'] = rep.meta['post_id']
            f['user_id'] = urls[0].split('/')[-1]
            if len(div.xpath('.//a//@href'))>2:
                f['parent_id'] = urls[1].split('/')[-1]
            yield f     
            priority = rep.meta.get('priority') or self.max_priority      
            yield Request(self.host+user_url,callback=self.parse_user,cookies=self.cookies,meta={'user_id': f['user_id'] ,\
            'priority':priority},priority=priority)
    def parse_comment(self,rep):        
        pages = rep.xpath('//body//input[@name="mp"]//@value').extract()
        if len(pages)>0:
            page_size = pages[0]         
            for i in xrange(int(page_size),0,-1):
                comment_url = rep.meta['comment_url'].split('#')[0]+'&page='+str(i)
                yield Request(comment_url,callback=self.parse_comment_by_page,cookies=self.cookies,meta={'post_id': rep.meta['post_id'],'priority':i},\
                priority=i)
        else:
            for c in  self.populate_comment(rep):
                yield c
    def parse_comment_by_page(self,rep):
        for c in  self.populate_comment(rep):
            yield c
    def populate_comment(self,rep):
        for div in rep.xpath('//body//div[contains(@id,"C_") and @class="c"]'):
            urls = div.xpath('.//a//@href').extract()
            user_url =  urls[0]
            c = Comment()
            c['content'] = div.xpath('.//span[@class="ctt"]//text()').extract()[0]
            c['platform'] = div.xpath('.//span[@class="ct"]//text()').extract()[0]
            c['post_id'] = rep.meta['post_id']
            c['user_id'] = urls[0].split('/')[-1]
            yield c
            priority = rep.meta.get('priority') or self.max_priority  
            yield Request(self.host+user_url,callback=self.parse_user,cookies=self.cookies,meta={'user_id': c['user_id'],\
            'priority':priority }, priority=priority)
       
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
        
        yield Request(url,callback=self.parse_user_further,cookies=self.cookies,meta=u,priority=(rep.meta.get('priority') or self.max_priority))
        
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
