from appium import webdriver
import os
import base64

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '5.1'
desired_caps['deviceName'] = '192.168.56.101:5555'
desired_caps['appPackage'] = 'com.android.settings'
desired_caps['appActivity'] = '.Settings'
# 声明driver对象
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)


# 安装apk到手机
# driver.install_app('/Users/panda/Desktop/app_test/开发者头条.apk')
# driver.install_app(os.getcwd() + os.sep + "开发者头条.apk")
# 卸载应用?driver.remove_app("io.manong.developerdaily")
#
# # 判断app是否已经安装
# if driver.is_app_installed("io.manong.developerdaily"):
#     driver.remove_app("io.manong.developerdaily")
# else:
#     driver.install_app(os.getcwd() + os.sep + "开发者头条.apk")

# 把本地文件传到手机
# with open("a.txt", "r") as f:
#     data = str(base64.b64encode(f.read().encode("utf-8")), "utf-8")
#     driver.push_file("/sdcard/hello.txt", data)

# 把手机里文件拉到本地
# orig_data = driver.pull_file("/sdcard/hello.txt")
# print(str(base64.b64decode(orig_data), "utf-8"))
# driver.quit()
# 获取页面源码
# print(driver.page_source)
if "设置" in  driver.page_source:
    print("找到啦！！！")
else:
    print("丢失了！！")
