from appium import webdriver
import os


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

# # 1. 获取手机时间
# print(driver.device_time)
# # 2. 获取手机宽高
# print(driver.get_window_size())
# # 3. 点按手机的按钮
# print(driver.keyevent(25))
# 4. 操作手机通知栏
# driver.open_notifications()
# 5. 获取当前手机网络
# print(driver.network_connection)
# # 6. 设置手机网络
# 0 无网络
# 1 飞行模式
# 2  wifi
# 4 数据
# 6 网线
driver.set_network_connection(1)
# print(driver.network_connection)
# 7. 截图
driver.get_screenshot_as_file(os.getcwd() + os.sep + 'hello.png')

driver.close_app()
driver.quit()