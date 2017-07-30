import pymongo
from DB.ISQLHelp import ISQLHelper
from SpiderNews.config import DB_CONFIG
import time

class MongoHelper(ISQLHelper):
    def __init__(self):
        self.client = pymongo.MongoClient(DB_CONFIG['DB_CONNECT_STRING'], connect=False)
    def init_db(self):
        newsTime = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        self.db = self.client.news
        self.news = self.db[newsTime]

    def drop_db(self):
        self.client.drop_database(self.db)

    def insert(self, value=None):
        if value:
            newsObj = dict(title=value['title'], content=value['content'], category=value['category'],secCategory=value['secCategory'],
                         img_path=value['image'],
                         time =value['time'], fromTO=value['from'],url=value['url'])
            self.news.insert(newsObj)

    def delete(self, conditions=None):
        if conditions:
            self.news.remove(conditions)
            return ('deleteNum', 'ok')
        else:
            return ('deleteNum', 'None')

    def update(self, conditions=None, value=None):
        # update({"UserName":"libing"},{"$set":{"Email":"libing@126.com","Password":"123"}})
        if conditions and value:
            self.news.update(conditions, {"$set": value})
            return {'updateNum': 'ok'}
        else:
            return {'updateNum': 'fail'}

    def select(self, count=None, conditions=None,page=None):
        if count:
            count = int(count)
        else:
            count = 0
        if conditions:
            conditions = dict(conditions)
            conditions_name = ['types', 'protocol']
            for condition_name in conditions_name:
                value = conditions.get(condition_name, None)
                if value:
                    conditions[condition_name] = int(value)
        else:
            conditions = {}
        items = self.news.find(conditions, limit=count).skip(int(page)).sort(
            [("time", pymongo.DESCENDING)])
        results = []
        for item in items:
            result = (item['title'], item['url'], item['category'])
            results.append(result)
        return results


if __name__ == '__main__':
    from DB.MongoHelp import MongoHelper as SqlHelper
    sqlhelper = SqlHelper()
    sqlhelper.init_db()
    # # print  sqlhelper.select(None,{'types':u'1'})
    # items= sqlhelper.proxys.find({'types':0})
    # for item in items:
    # print item
    # # # print sqlhelper.select(None,{'types':u'0'})
    pass
