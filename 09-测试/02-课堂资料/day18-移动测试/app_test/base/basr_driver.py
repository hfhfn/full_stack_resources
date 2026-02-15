from appium import webdriver


def init_driver(APPPackage, APPActivity):
    devices_info = {}
    devices_info["platformName"] = "Android"
    devices_info["platformVersion"] = "5.1"
    devices_info["deviceName"] = '192.168.56.101:5555'
    # app信息
    devices_info['appPackage'] = APPPackage
    devices_info['appActivity'] = APPActivity
    devices_info["unicodeKeyboard"] = True
    devices_info["resetKeyboard"] = True

    # 驱动信息
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', devices_info)
    return driver