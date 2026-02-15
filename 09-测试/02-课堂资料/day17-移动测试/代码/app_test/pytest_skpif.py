# 跳过指定的测试函数

import pytest

#
# class Test_ABC(object):
#     def test_a(self):
#         print("test-a在执行")
#
#     def test_b(self):
#         print("test-b在执行")
#
#     @pytest.mark.skipif(condition=2>1, reason="2大于1")
#     def test_c(self):
#         print("test-c在执行")


# class Test_ABC:
#     def setup_class(self):
#         print("\nsetup")
#
#     def teardown_class(self):
#         print("\nteardown")
#
#     def test_a(self):
#         print("test_a")
#
#     # @pytest.mark.skipif(condition=1>2, reason="跳过")
#     def test_b(self):
#         print("test_b")
#         assert 0

# =标记为预期失败函数
# class Test_ABC:
#     def setup_class(self):
#         print("\nsetup")
#
#     def teardown_class(self):
#         print("\nteardown")
#
#     def test_a(self):
#         print("\ntest_a")
#
#     @pytest.mark.xfail(condition=2>1, reason="跳过")
#     def test_b(self):
#         print("\ntest_b")
#         assert 0

# 参数化
class Test_ABC:
    def setup_class(self):
        print("\nsetup")

    def teardown_class(self):
        print("\nteardown")

    def test_a(self):
        print("\ntest_a")

    @pytest.mark.parametrize("a", [(3, 4),(5,6)])
    def test_b(self, a):
        print("\ntest_b的值是%s", a)
        # assert 0