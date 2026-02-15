"""
查找的元素定位信息
"""
from selenium.webdriver.common.by import By

# 新增信息按钮
add_btn = (By.ID, "com.android.mms:id/action_compose_new")
# 接收者按输入框
receiver_number = (By.ID, "com.android.mms:id/recipients_editor")
# 输入内容框
send_sms = (By.ID, "com.android.mms:id/embedded_text_editor")
# 发送按钮
send_btn = (By.ID, "com.android.mms:id/send_button_sms")

# 接收短信的手机号
receive_phone_number = "13612345678"

# 发送的短信内容
send_sms_message = ["哈俄哈哈帮助","葫芦娃大战孙悟空", "关羽战秦琼"]