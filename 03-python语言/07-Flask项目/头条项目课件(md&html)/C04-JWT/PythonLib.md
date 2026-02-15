# JWT的Python库-pyjwt

[TOC]

<!-- toc -->

## 1. 独立的JWT Python库

> [pyjwt](https://pyjwt.readthedocs.io/en/latest/)安装时叫做`pyjwt`，但是在导包时是`jwt`

### 1.1 安装

> ```shell
> pip install pyjwt
> ```

### 1.2 用例

> ```python
> import jwt
> from jwt import PyJWTError
> from datetime import datetime, timedelta
> 
> # 构造并包装数据
> # payload 载荷，即数据
> # exp 过期时间，要求使用格林尼治时间
> payload = {'payload': 'test',
>            'exp': datetime.utcnow() + timedelta(seconds=30)}
> # 秘钥
> key = 'secret'
> # 生成token
> token = jwt.encode(payload, key, algorithm='HS256')
> print(token)
> 
> # 验证
> try:
>     # pyjwt内部对有效期进行了验证，过期就报错
>     ret = jwt.decode(token, key, algorithms='HS256')
>     print(ret)
> except PyJWTError as e:
>     print('jwt认证失败')
> ```

## 2. 头条项目封装

> 代码位置：`项目路径/common/utils/jwt_util.py`
>
> ```python
> import jwt
> from flask import current_app
> 
> 
> def generate_jwt(payload, expiry, secret=None):
>     """
>     生成jwt
>     :param payload: dict 载荷
>     :param expiry: datetime 有效期
>     :param secret: 密钥
>     :return: jwt
>     """
>     _payload = {'exp': expiry}
>     _payload.update(payload) # _payload['payload'] = 'xxxx'
> 
>     if not secret:
>         secret = current_app.config['JWT_SECRET']
> 
>     token = jwt.encode(_payload, secret, algorithm='HS256')
>     return token.decode()
> 
> 
> def verify_jwt(token, secret=None):
>     """
>     检验jwt，返回pyload字典
>     :param token: jwt
>     :param secret: 密钥
>     :return: dict: payload
>     """
>     if not secret:
>         secret = current_app.config['JWT_SECRET']
> 
>     try:
>         payload = jwt.decode(token, secret, algorithm=['HS256'])
>     except jwt.PyJWTError:
>         payload = None
> 
>     return payload
> 
> ```



