from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import time


desired_caps = {}
# 设备信息
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '5.1'
desired_caps['deviceName'] = '192.168.56.101:5555'
# app的信息
desired_caps['appPackage'] = 'com.android.launcher3'
desired_caps['appActivity'] = '.Launcher'

# 声明我们的driver对象
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

# 点击知道了
kn = driver.find_element_by_xpath("//*[contains(@text, '知道了')]").click()

if "设置" in driver.page_source:
    # 点击设置
    driver.find_element_by_xpath("//*[contains(@text, '设置')]").click()
    time.sleep(4)
    # 点击安全
    more = driver.find_element_by_xpath("//*[contains(@text, '更多')]").location
    time.sleep(3)
    battery = driver.find_element_by_xpath("//*[contains(@text, '电池')]").location
    time.sleep(3)
    driver.swipe(battery['x'], battery['y'], more['x'], more['y'])
    time.sleep(3)
    driver.find_element_by_xpath("//*[contains(@text, '安全')]").click()
    # 点击屏幕锁定方式
    time.sleep(3)
    driver.find_element_by_xpath("//*[contains(@text, '屏幕锁定方式')]").click()
    # 点击图案
    time.sleep(3)
    driver.find_element_by_xpath("//*[contains(@text, '图案')]").click()
    # 绘制图案
    time.sleep(3)
    point_class = driver.find_element_by_class_name("android.view.View")
    time.sleep(3)
    TouchAction(driver).press(x=183, y=953).wait(100)\
        .move_to(x=280, y=0).wait(100).move_to(x=0, y=-280).wait(100).move_to(x=0, y=-280).wait(100).\
        move_to(x=280, y=0).release().perform()

else:
    print("设置按钮找不到！！")

driver.close_app()
driver.quit()