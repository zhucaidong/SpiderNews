#encoding=utf-8
import scrapy
import time
import SpiderNews.config

from SpiderNews.items import NewsSpiderItem
class TouTiaoNews(scrapy.Spider):
    name='toutiao'
    allowed_domains = ["toutiao.com"]
    start_urls = [
        'http://toutiao.com/articles_news_society/p1'
    ]
    maxpage = 10
    base_class_url = 'http://toutiao.com/articles_news_society'
    base_url = 'http://toutiao.com'
    category = ['articles_news_society', 'articles_news_entertainment',
                'articles_movie', 'articles_news_tech', 'articles_digital',
                'articels_news_sports', 'articles_news_finance', 'articles_news_military',
                'articles_news_culture', 'articles_science_all'
                ]
    def parse(self,response):
        for ctg in self.category :
            for page in range(0,self.maxpage):
                url = self.base_url+'/'+ctg+'/p'+str(page)
                header=SpiderNews.config.get_header()
                header['referer:'] = url
                header['Host:'] = 'www.toutiao.com'
                #header['cookie:'] = 'UM_distinctid=15d607a2e6e27f-0b568b7380dccd-38700257-100200-15d607a2e6f617; uuid="w:c23dea8de3794e4e8e4f4daf29d0fb4f"; csrftoken=e93e5a87ead01d5d3af964a1875d88a1; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6444865594025739789; CNZZDATA1259612802=991403685-1500559874-https%253A%252F%252Fwww.baidu.com%252F%7C1500721426'
                print(header)
                yield scrapy.Request(url,self.parseNewsHref,headers=header)
                # 解析具体新闻内容

    def parseNews(self, response):
        articles = response.xpath("//div[@id='pagelet-article']")
        item = NewsSpiderItem()
        title = articles.xpath("//div[@class='article-header']/h1/text()").extract()[0]
        tm = articles.xpath("//div[@id='pagelet-article']//span[@class='time']/text()").extract()[0]
        content = articles.xpath("//div[@class='article-content']//p/text()").extract()

        if (len(title) != 0 and len(tm) != 0 and len(content) != 0):
            item['title'] = title
            item['time'] = int(time.mktime(time.strptime(tm, '%Y-%m-%d %H:%M')))
            item['url'] = response.url
            cc = ''
            if (len(content) != 0):
                for c in content:
                    cc = cc + c + '\n'
                item['content'] = cc
                yield item

    def printC(self, text):
        for t in text:
            print (t.encode('utf-8'))