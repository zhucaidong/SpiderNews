from selenium import webdriver
from lxml import etree
browser = webdriver.PhantomJS()
browser.get('https://www.toutiao.com/ch/news_hot/')
browser.implicitly_wait(10)
print(browser.page_source)