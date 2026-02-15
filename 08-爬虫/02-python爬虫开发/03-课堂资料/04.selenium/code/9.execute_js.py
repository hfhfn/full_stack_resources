#coding:utf-8
from selenium import webdriver


url = 'https://qd.lianjia.com/'

driver = webdriver.Chrome()


driver.get(url)

js = 'scrollTo(0,500)'

driver.execute_script(js)


driver.find_element_by_xpath('/html/body/div[2]/ul/li[1]/a/img').click()