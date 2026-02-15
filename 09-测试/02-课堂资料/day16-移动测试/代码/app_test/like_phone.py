from appium import webdriver
import  time

from appium.webdriver.common.touch_action import TouchAction

desired_caps = {}
# 设备信息
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '5.1'
desired_caps['deviceName'] = '192.168.56.101:5555'
# app的信息
desired_caps['appPackage'] = 'com.android.settings'
desired_caps['appActivity'] = '.Settings'

# 声明我们的driver对象
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

# 1. 手指轻敲操作
# more = driver.find_element_by_xpath("//*[contains(@text, '更多')]")
# TouchAction(driver).tap(more, more.location['x'], more.location['y']).perform()
# time.sleep(3)
# 2. 手指按下操作
# battery = driver.find_element_by_xpath("//*[contains(@text, '电池')]")
# TouchAction(driver).press(battery, battery.location['x'], battery.location['y']).perform()
# time.sleep(3)
# 3. 等待操作
# wlan = driver.find_element_by_xpath("//*[contains(@text, 'WLAN')]").click()
# id = driver.find_element_by_xpath("//*[contains(@text, 'WiredSSID')]")
# TouchAction(driver).press(id, id.location['x'], id.location['y']).wait(3000).release().perform()
# 4. 手指长按操作
# wlan = driver.find_element_by_xpath("//*[contains(@text, 'WLAN')]").click()
# id = driver.find_element_by_xpath("//*[contains(@text, 'WiredSSID')]")
# TouchAction(driver).long_press(id, id.location['x'], id.location['y'], 3000).release().perform()
# 5. 手指移动操作
wlan = driver.find_element_by_xpath("//*[contains(@text, 'WLAN')]").location
safe = driver.find_element_by_xpath("//*[contains(@text, '安全')]").location

driver.swipe(safe['x'], safe['y'], wlan['x'], wlan['y'])
time.sleep(3)
date_btn = driver.find_element_by_xpath("//*[contains(@text, '日期和时间')]")
print(date_btn.location)
# 必须要release否则报错
TouchAction(driver).long_press(date_btn).move_to(date_btn).release().perform()
driver.close_app()
driver.quit()
