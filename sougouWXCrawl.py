from selenium import webdriver
from lxml import etree
import time

browser = webdriver.PhantomJS()
browser.get('http://weixin.sogou.com/')
browser.implicitly_wait(5)

recomment = browser.find_element_by_id('pc_1')
recomment.click()
print(browser.page_source)

