import scrapy
from SpiderNews.config import NEWS_TYPE,get_header
from SpiderNews.items import NewsSpiderItem
from scrapy import log
from selenium import webdriver


class NetEaseSpider(scrapy.Spider):
    start_urls = ['http://news.baidu.com']
    name = 'baiduindex'
    allowed_domains = ['news.baidu.com']
    base_url = 'http://news.baidu.com/'

    def parse(self, response):
                    yield scrapy.Request(self.base_url,self.parseNewsPage,headers=get_header())

    def parseList(self, response):
        urls = response.xpath("//a/@href").extract()
        for url in urls:
            yield scrapy.Request(url, self.parseNews)

    def parseNewsPage(self, response):
        log.msg(type(response), level=log.WARNING)
        item = NewsSpiderItem()
        #首页热点新闻模块
        news_url = response.xpath("//li/a/@href").extract()
        news_text = response.xpath("//li/a/text()").extract()

        print(news_url)
        print(news_text)

        pane_news_url = response.xpath("//div[@id='pane-news']//li/a/@href").extract()
        pane_news_text = response.xpath("//div[@id='pane-news']//li/a/text()").extract()
        local_news_url = response.xpath("//div[@id='local_news']//li/a/@href").extract()
        print(local_news_url)

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
