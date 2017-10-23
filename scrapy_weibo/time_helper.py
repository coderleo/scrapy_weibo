#coding=utf-8
import time
import datetime
def format_time(source):
    source = source.replace('&nbsp;',' ')
    content = source.split(' ')
    if u'小时前' in content[0]:
        t = source.replace(u'小时前','')
        return datetime.datetime.now() - datetime.timedelta(hours = int(t))
    if u'分钟前' in content[0]:
        t = source.replace(u'分钟前','')
        return datetime.datetime.now() - datetime.timedelta(minutes = int(t))

    if u'今天' in content[0]:
        t = time.strftime('%Y-%m-%d',time.localtime(time.time()))+' '+content[1][0:5]+':00'
        t = t.replace(u'\xa0', u'')
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(t,"%Y-%m-%d %H:%M:%S")))
      
    if u'月' in content[0] and u'日' in content[0]:
        t= time.strftime('%Y-',time.localtime(time.time()))+ \
        content[0].replace(u'月','-').replace(u'日','')+' '+content[1][0:5]+':00'
        t = t.replace(u'\xa0', u'')
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(t,"%Y-%m-%d %H:%M:%S")))
    if '-' in content[0]:
        
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(content[0].replace(u'\xa0', u'')+' '+content[1][0:8].replace(u'\xa0', u''),"%Y-%m-%d %H:%M:%S"))) 
    
    return None

def current_time():
    return datetime.datetime.now() 
    #return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))[leo@localhost core]$ 
