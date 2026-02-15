from  appium import webdriver
import pytest



class Test_ABC(object):

    def setup_class(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.1'
        desired_caps['deviceName'] = '192.168.56.101:5555'
        desired_caps['appPackage'] = 'com.android.settings'
        desired_caps['appActivity'] = '.Settings'
        # 声明driver对象
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

    def teardown_class(self):
        self.driver.close_app()
        self.driver.quit()

    def test_a(self):
        self.driver.find_element_by_xpath("//*[contains(@text,'WLA')]").click()
        print("askdjfjsdghgvburyi")






