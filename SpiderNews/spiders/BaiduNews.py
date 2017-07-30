import scrapy
from SpiderNews.config import NEWS_TYPE,get_header
from SpiderNews.items import NewsSpiderItem
from scrapy import log


class NetEaseSpider(scrapy.Spider):
    start_urls = ['http://news.baidu.com/ent']
    name = 'baidu'
    allowed_domains = ['news.baidu.com']
    base_url = 'http://news.baidu.com/'
    urls={'guonei' : 'http://news.baidu.com/guonei',
          'guoji' : 'http://guoji.news.baidu.com/',
         'internet' : 'http://news.baidu.com/internet',
         'ent':'http://news.baidu.com/ent',
    }

    def parse(self, response):
        for url_key in self.urls.keys():
                    url = self.urls.get(url_key)
                    print(url_key)
                    yield scrapy.Request(url,self.parse_instat_news,headers=get_header())

    def parseList(self, response):
        urls = response.xpath("//a/@href").extract()
        for url in urls:
            yield scrapy.Request(url, self.parseNews)

    def parseNews(self, response):
        #print(response.url)
        log.msg(type(response), level=log.WARNING)
        item = NewsSpiderItem()
        focusUrl = response.xpath("//div[@id='col_focus']//li/a/@href").extract()
        focusText = response.xpath("//div[@id='col_focus']//li/a/text()").extract()
        self.parse_instat_news(response)
        for i in range(1,len(focusUrl)+1):
                   item['url'] = focusUrl[i]
                   item['title'] = focusText[i]
                   item['category'] =  ''
                   item ['secCategory'] = 'focus'
                   yield item

        #print(focusText)
        #print (focusUrl)
    def parse_instat_news(self,response):
        attimeUrl = response.xpath("//div[@id='instant-news']//li/a/@href").extract()
        attimeText = response.xpath("//div[@id='instant-news']//li/a/text()").extract()
        item = NewsSpiderItem()
        for i in range(1, len(attimeUrl) + 1):
            item['url'] = attimeUrl[i]
            item['title'] = attimeText[i]
            item['category'] = ''
            item['secCategory'] = 'attime'
            yield item
        '''
        titles = response.xpath("//a/text()").extract()
        url = response.xpath("//a/@href").extract()
        for i in range(1,len(titles)):
            item['title'] = titles[i]
            item['url'] = url[i]
            item['category'] = 'ent'
            yield item'''
        #timee = data.xpath("//div[@class='post_time_source']/text()").extract()
        #title = data.xpath("//h1/text()").extract()
        #content = data.xpath("//div[@class='post_text']/p/text()").extract()
