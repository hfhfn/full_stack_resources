from appium import webdriver
import  time


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

# 1. 滑动事件
# driver.swipe(262, 444, 355, 2220, 3000)
# wlan_location = driver.find_element_by_xpath("//*[contains(@text, 'WLAN')]").location
# safe_location = driver.find_element_by_xpath("//*[contains(@text, '安全')]").location
# driver.swipe(safe_location['x'], safe_location['y'], wlan_location['x'], wlan_location['y'], 3000)
# time.sleep(3)
# 2. 滚动事件
# wlan_location = driver.find_element_by_xpath("//*[contains(@text, 'WLAN')]")
# safe_location = driver.find_element_by_xpath("//*[contains(@text, '安全')]")
# driver.scroll(safe_location, wlan_location)
# 3. 拖拽事件
# wlan_location = driver.find_element_by_xpath("//*[contains(@text, 'WLAN')]")
# safe_location = driver.find_element_by_xpath("//*[contains(@text, '安全')]")
# driver.drag_and_drop(safe_location, wlan_location)
# time.sleep(3)
# 4. 应用置于后台
driver.background_app(5)

driver.close_app()
driver.quit()