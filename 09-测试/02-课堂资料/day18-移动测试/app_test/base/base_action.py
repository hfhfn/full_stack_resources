class BaseAction(object):
    def __init__(self, driver):
        self.driver = driver

    def click_element(self, loc):
        """点击的基本操作"""
        return self.find_element(loc).click()

    def input_element_content(self, loc, content):
        """输入框的基本操作"""
        return self.find_element(loc).clear().send_keys(content)


    def find_element(self, ele):
        return self.driver.find_element(ele[0], ele[1])