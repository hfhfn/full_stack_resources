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
# 输入汉字要加上
desired_caps['unicodeKeyboard'] = True
desired_caps['resetKeyboard'] = True

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
# 根据元素获取属性值
# 需求： 在搜索框输入要搜索的内容
# 发送数据到输入框
# 1. 打开设置

# 2. 点击搜索按钮
# driver.find_element_by_id("com.android.settings:id/search").click()
# 3. 输入内容
# btn = driver.find_element_by_id("android:id/search_src_text")
#
# btn.send_keys("无线")
# time.sleep(3)
# # 清空输入框内容
# btn.clear()
# time.sleep(3)




# 获取元素的值
# print(driver.find_elements_by_id("com.android.settings:id/title")[0].text)
# 获取属性值
# print(driver.find_elements_by_id("com.android.settings:id/title")[0].get_attribute("resourceId"))



# 获取坐标
print(driver.find_element_by_xpath("//*[contains(@text, '设置')]").location["x"])
# 获取启动的包名和启动名
print(driver.current_activity)
print(driver.current_package)

driver.close_app()
driver.quit()