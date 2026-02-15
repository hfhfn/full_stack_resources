from appium import webdriver
import os, time
import base64

from selenium.webdriver.support.wait import WebDriverWait

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '5.1'
desired_caps['deviceName'] = '192.168.56.101:5555'
desired_caps['appPackage'] = 'com.android.settings'
desired_caps['appActivity'] = '.Settings'
# 声明driver对象
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

# 元素的定位
# id， class  xpath
# 点击wlan
# driver.find_element_by_xpath("//*[contains(@text, 'WLAN')]").click()
#
# # driver.find_element_by_id("com.android.settings:id/title").click()
# # 返回
# driver.find_element_by_class_name("android.widget.ImageButton").click()

# 查找一组元素
# print(driver.find_elements_by_class_name("android.widget.TextView"))
# # 强制等待
# time.sleep(4)
# 显示等待
# try:
#     WebDriverWait(driver, 5, 1).until(lambda x: x.find_element_by_xpath("//*[contains(@text, '设置xcvb')]"))
#     print("找到了")
# except:
#     print("超时了")

# 隐士等待, 所有操作都会默认等待3s
driver.implicitly_wait(3)
driver.find_element_by_xpath("//*[contains(@text, 'WLAN')]").click()

# print(driver.find_elements_by_id("com.android.settings:id/title"))
# print(driver.find_elements_by_xpath("//*[contains(@text, '设置')]"))
driver.close_app()
driver.quit()