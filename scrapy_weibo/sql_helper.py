#coding=utf-8
import MySQLdb
from .db_config import MySQLConfig

class SqlHelper:
    def __init__(self,*args):
        if len(args)>0:
            self.config = args[0]
        else:
            self.config = MySQLConfig
        self.con =  MySQLdb.connect(**self.config)

    def get_cursor(self):        
        return self.con.cursor()
        
    def select_keyword(self):
        cur = self.get_cursor()
        try:
            cur.execute('SELECT ID,rule FROM pdi_manager.di_keyword_class where level=3')
            for row in cur:
                rules = row[1].replace('&&','').split(',')
                for rule in rules:
                    yield (row[0],rule)
        except Exception,e:
            print "select_keyword error: %s", e
        finally:
            cur.close()
        

    def insert_post(self,values):
        cur = self.get_cursor()
        try:
          
            cur.executemany('insert into  pdi_data.weibo_posts(id,userid,content,repostcount,thumbcount,commentcount,createdtime,scrapy_flag\
            ,platform) values(%s, %s, %s, %s,%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE repostcount=values(repostcount),thumbcount=values(thumbcount),\
            commentcount=values(commentcount)', [value[0] for value in values])
            cur.executemany('insert ignore into pdi_manager.di_mapping_weibo_keyword(wid,kid) values(%s, %s)', [value[1] for value in values])
            self.con.commit()
        except Exception,e:
            print "insert_post error: %s", e
        finally:
            cur.close()
    def insert_user(self,values):
        cur = self.get_cursor()
        try:
          
            cur.executemany('insert into  pdi_data.weibo_users(id,description,nickname,gender,labels,auth,birthday,focuscount\
            ,weibocount,fanscount) values(%s, %s, %s, %s,%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE focuscount=values(focuscount),weibocount=values(weibocount),\
            fanscount=values(fanscount)', [value[0] for value in values])
         
            self.con.commit()
        except Exception,e:
            print "insert_post error: %s", e
        finally:
            cur.close()
