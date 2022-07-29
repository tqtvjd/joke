# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

from itemadapter import ItemAdapter

class JokePipeline(object):

    jokeList = []

    def open_spider(self, spider):
        self.file = open('jokes.json', 'a', encoding='utf-8')

    def close_spider(self, spider):
        if len(self.jokeList) in range(1,19):
            print(*self.jokeList)
            self.write_json()
        self.file.close()

    def __init__(self):
        pass

    def process_item(self, item, spider):
        self.jokeList.append(ItemAdapter(item).asdict())
        if len(self.jokeList) == 20:
            self.write_json()  
        return item
    
    def write_json(self):
        line = json.dumps(self.jokeList, ensure_ascii=False) + "\n"
        self.file.write(line)
        self.jokeList.clear()

