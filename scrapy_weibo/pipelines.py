# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
class ScrapyWeiboPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = codecs.open('items.jl', 'w',encoding='utf8')
        self.file_user = codecs.open('user.jl', 'w',encoding='utf8')
        self.file_forward = codecs.open('forward.jl','w',encoding='utf8')
    def process_item(self, item, spider):
        
        if 'Post' in str(item.__class__):
            line = json.dumps(dict(item),indent=4, ensure_ascii=False) + "\n"
            self.file.write(line)
        if 'User' in str(item.__class__):
            line = json.dumps(dict(item),indent=4, ensure_ascii=False) + "\n"
            self.file_user.write(line)
        if 'Comment' in str(item.__class__):
            line = json.dumps(dict(item),indent=4, ensure_ascii=False) + "\n"
            self.file_forward.write(line)
        return item
