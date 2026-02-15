from flask import g,jsonify
import functools
# 1、封装工具，/lib/decoraters.py
# 2、定义装饰器
# 3、判断用户id是否存在，从g对象中尝试获取用户id
# 4、返回结果

def login_required(func):

    # 作用：让被装饰器的装饰的函数的属性(函数名)不发生变化。
    @functools.wraps(func)
    def wrapper(*args,**kwargs):
        if not g.user_id:
            return jsonify(msg='token error'),401
        return func(*args,**kwargs)
    # wrapper.__name__ = func.__name__
    return wrapper

