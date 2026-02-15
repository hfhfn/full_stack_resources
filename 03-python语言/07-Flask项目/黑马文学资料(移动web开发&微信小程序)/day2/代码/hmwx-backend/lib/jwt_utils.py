import jwt
# 导入current_app，获取配置信息
from flask import current_app
# jwt工具的封装
# 步骤：
# 1.导入jwt模块
# 2.封装jwt生成的函数，必须要有密钥secret_key
# 3.封装jwt校验的函数


def generate_jwt(payload,expire,secret_key=None):
    # 参数：
    # payload表示存储的用户信息
    # expire表示jwt的过期时间
    # secret_key表示密钥
    _payload = {'exp':expire}
    _payload.update(payload)
    # 判断是否传入密钥
    if not secret_key:
        secret_key = current_app.config['SECRET_KEY']
    token = jwt.encode(_payload,secret_key,algorithm='HS256')
    return token.decode()
    pass


def verify_jwt(token,secret_key=None):
    # 参数：
    # token表示需要校验的jwt/token
    # secret_key表示密钥
    if not secret_key:
        secret_key = current_app.config.get('SECRET_KEY')
    try:
        payload = jwt.decode(token,secret_key,algorithms=['HS256'])
    except jwt.PyJWTError:
        payload = None

    return payload
    pass

