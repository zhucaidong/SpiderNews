from selenium import webdriver
from lxml import etree
import time
from DB.MongoHelp import MongoHelper as SqlHelper

SqlH= SqlHelper()
SqlH.init_db()
type = ('focus-top','local_news','guonei','guojie','caijing','yule','tiyu','col-auto','col-house','hulianwang','internet-plus','col-tech','col-edu','col-game','col-discovery','col-healthy','col-lady','shehui','junshi','tupianxinwen')
browser = webdriver.PhantomJS()
browser.get('http://news.baidu.com/')
js1 = 'return document.body.scrollHeight'
js2 = 'window.scrollTo(0, document.body.scrollHeight)'
old_scroll_height = 0
while(browser.execute_script(js1) > old_scroll_height):
    old_scroll_height = browser.execute_script(js1)
    browser.execute_script(js2)
    time.sleep(0.8)
html = browser.page_source
tree=etree.HTML(html)
updatetime = time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))
print(updatetime)
for item in type:
    regularExpressionUrl ='//div[@id="'+item+'"]//li/a/@href'
    regularExpressionText = '//div[@id="'+item+'"]//li/a/text()'
    news_url = tree.xpath(regularExpressionUrl)
    news_text = tree.xpath(regularExpressionText)
    #print('url_len'+str(len(news_url)))
   # print('text_len'+str(len(news_text)))
    for i in range(0,len(news_text)):
     if 'http' in news_url[i]:
        newsContent  = {'title': news_text[i], 'url': news_url[i], 'content': '', 'category': item,
           'secCategory': '', 'image': '', 'time': updatetime, 'from': ''}
        count = SqlH.select(1, {'title': news_text[i]})
        #print(count)
        if len(count) == 0:
            SqlH.insert(newsContent)

    #print(item)
    #print(news_text)
    #print(news_url)
# 首页热点新闻模块

browser.quit()

