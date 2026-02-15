import pytest
import os
import sys
print(sys.path)
sys.path.append(os.getcwd())
import base

from base.basr_driver import init_driver
from page.send_sms import SendSMS


class TestSmsSending(object):
    def setup_class(self):
        # 抽取基本的驱动信息
        self.driver = init_driver(base.APPPackage, base.APPActivity)
        # 发送短信
        self.send_sms = SendSMS(self.driver)

    def teardown_class(self):
        self.driver.close_app()
        self.driver.quit()

    def test_send_sms(self):
        # 定位到新增
        self.send_sms.click_add()
        # 加入等待时间, 隐士等待时间
        self.driver.implicitly_wait(5)
        # 接收者
        self.send_sms.click_receiver()
        # 发送短信
        self.send_sms.sending_sms()






