from base.base_action import BaseAction
from . import constans

# class SendSMS(object):
class SendSMS(BaseAction):
    def __init__(self, driver):
        # self.driver = driver
        # self.base_action = BaseAction(driver)
        BaseAction.__init__(self, driver)

    def click_add(self):
        """新增"""
        # 2. 定位到新增
        self.driver.implicitly_wait(5)
        try:
            # self.find_element(constans.add_btn).click()
            # 点击新增短信按钮
            self.click_element(constans.add_btn)
        except Exception as e:
            print(e)

        # self.driver.find_element_by_id("com.android.mms:id/action_compose_new").click()

    def click_receiver(self):
        """定位到接收者"""
        # 3.定位接收者元素
        # receive_number = self.driver.find_element_by_id("com.android.mms:id/recipients_editor")
        # receive_number = self.find_element(constans.receiver_number)
        # # receive_number = self.driver.find_element_by_xpath("//*[contains(@text, '接收者')]")
        # # 4.涉及到输入框的先clear 在输入
        # receive_number.clear()
        # receive_number.send_keys("13812345678")

        self.input_element_content(constans.receiver_number, constans.receive_phone_number)

    def sending_sms(self):
        """发送短信"""
        send_list = constans.send_sms_message
        # 5.定位到发送元素
        send_sms = self.find_element(constans.send_sms)
        # send_sms = self.driver.find_element_by_id("com.android.mms:id/embedded_text_editor")
        send_btn = self.find_element(constans.send_btn)
        # send_btn = self.driver.find_element_by_id("com.android.mms:id/send_button_sms")
        # 6.遍历发送的信息
        for i in send_list:
            send_sms.clear()
            send_sms.send_keys(i)
            send_btn.click()



