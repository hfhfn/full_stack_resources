import pytest

class Test_ABC(object):
    # 函数级别的set_up和teardown使用,无论失败还是成功，
    # setup和teardown每个函数都会执行一次

    # def setup(self):
    #     print("setup_method")
    #
    # def teardown(self):
    #     print("teardown_method")
    #
    # def test_a(self):
    #     print("test_a")
    #     assert 1
    #
    # def test_b(self):
    #     print("test_b")
    #
    # def test_c(self):
    #     print("test_c")
    #     assert  0

    # 类级别的使用
    # setup和teardown只运行一次
    def setup_class(self):
        print("setup_method")

    def teardown_class(self):
        print("teardown_method")

    def test_a(self):
        print("test_a")
        assert 1

    def test_b(self):
        print("test_b")

    def test_c(self):
        print("test_c")
        assert 0

