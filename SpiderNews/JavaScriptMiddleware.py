# -*- coding: utf-8 -*-
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
import requests
from scrapy.downloadermiddlewares.stats import DownloaderStats

global driver
driver = webdriver.PhantomJS()  # 指定使用的浏览器，写在此处而不写在类中，是为了不每次调用都生成一个信息独享，减少内存使用
print ("PhantomJS is starting...")


class JavaScriptMiddleware(object):
    def process_request(self, request, spider):
        global driver
        # driver = webdriver.Firefox()
        url = request.url;
        # driver.get(url)
        # time.sleep(1)
        js = "var q=document.documentElement.scrollTop=10000"
        driver.execute_script(js)  # 可执行js，模仿用户操作。此处为将页面拉至最底端。
        # body = driver.page_source
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; windows NT)'
        headers = {'User-Agent': user_agent}
        r = requests.post(url, headers=headers)
        body = r.content
        print("访问" + request.url)
        return HtmlResponse(url, encoding='utf-8', status=200, body=body)
        # return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)