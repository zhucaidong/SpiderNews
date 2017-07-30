# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
from SpiderNews.items import TitleSpiderItem
import threading
import sys
from DB.MongoHelp import MongoHelper

from DB.MongoHelp import MongoHelper as SqlHelper



sys.path.append("..")
class SpidernewsPipeline(object):
    def process_item(self, item, spider):
        return item


class NewsSpiderPipeline(object):
    lock = threading.Lock()
    #file = open(Global.content_dir, 'a')


    def __init__(self):
        pass
        self.sqlhelper = SqlHelper()
        self.sqlhelper.init_db()

    def process_item(self, item, spider):
            Val = {'title': item['title'],'url':item['url'], 'content': 'ddd', 'category': item['category'],'secCategory':item['secCategory'], 'image': 'ttt', 'time': 'fff', 'from': 'eee'}
            count = self.sqlhelper.select(1,{'title':item['title']})
            print(count)
            if len(count) == 0 :
                self.sqlhelper.insert(Val)
                return item
    '''line = json.dumps(dict(item)) + '\n'
        try:
            NewsSpiderPipeline.lock.acquire()
            NewsSpiderPipeline.file.write(line)
        except:
            pass
        finally:
            NewsSpiderPipeline.lock.release()'''

    def spider_closed(self, spider):
        pass