from flask import request,g
from .jwt_utils import verify_jwt

# 请求钩子：
# - 1.封装工具，/lib/middlewrares.py
# - 2.定义函数，获取用户头信息，Authorization
# - 3.使用jwt工具，校验token，从payload中提取用户id，把用户id赋值给g对象
# @app.before_request
# app.before_request(before_request)

def before_request():
    g.user_id = None
    auth = request.headers.get('Authorization')
    if auth:
        payload = verify_jwt(token=auth)
        if payload:
            g.user_id = payload.get("user_id")