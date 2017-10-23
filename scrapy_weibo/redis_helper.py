import redis
from time import sleep
class RedisHelper(object):
    def __init__(self):
        self.db =  redis.Redis(host='127.0.0.1',port=6379,db=0)
        self.redis_namespace = 'url'
    def push(self,item):
        self.db.lpush(self.redis_namespace,item)
    def pop(self):
        while True:
            task = self.db.blpop(self.redis_namespace,0)
            yield task[1]
            print "Task get", task
            sleep(0.1)