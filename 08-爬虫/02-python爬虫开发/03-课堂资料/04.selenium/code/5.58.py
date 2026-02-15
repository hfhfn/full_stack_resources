#coding:utf-8
from selenium import webdriver


# 1.创建浏览器对象
driver = webdriver.Chrome()

# 2.操作浏览器对象
driver.get('https://lfyanjiao.58.com/hezu/?PGTID=0d100000-0320-44c6-c018-2374633dc940&ClickID=2')


el_list = driver.find_elements_by_xpath('/html/body/div[5]/div/div[5]/div[2]/ul/li/div[2]/h2/a')

# print(len(el_list))
# print(el_list)

for el in el_list:
    print(el.text,el.get_attribute('href'))


# el.send_keys(data), 该元素必须能够接受数据 input/text
# el.click()    该元素必须能够接受点击操作

