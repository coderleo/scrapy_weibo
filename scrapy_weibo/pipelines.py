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

    def process_item(self, item, spider):
        line = json.dumps(dict(item),indent=4, ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
