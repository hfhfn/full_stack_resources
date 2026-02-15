# 头条项目实施方案

[TOC]

<!-- toc -->

## 1. 需求

> 设置有效期，但有效期不宜过长，需要刷新。
>
> 如何解决刷新问题？
>
> - 手机号+验证码（或帐号+密码）验证后颁发接口调用token与refresh_token（刷新token）
>
> - Token 有效期为2小时，在调用接口时携带，每2小时刷新一次 
>
> - 提供refresh_token，refresh_token 有效期14天 
>
> - 在接口调用token过期后凭借refresh_token 获取新token
>
> - 未携带token 、错误的token或接口调用token过期，返回401状态码
>
> - refresh_token 过期返回403状态码，前端在使用refresh_token请求新token时遇到403状态码则进入用户登录界面从新认证。
>
> - token的携带方式是在请求头中使用如下格式：
>
>   > `Bearer `表示后边就是token，行业规定
>
>   ```http
>   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg
>   ```
>
>   注意：Bearer前缀与token中间有一个空格

## 2. 实现

> 该需求需要我们实现以下功能代码
>
> - 注册或登录时获取token
> - 完成请求钩子
>   - 实现在处理每个请求之前能够从token中拿到用户相关信息，并且知道该token是否为refresh_token
> - 强制登录装饰器
>   - 一旦没有token并且也没有refresh_token，就强制用户进入登录/注册页面
> - 更新token接口
>   - 如果是refresh_token就更新token

### 2.1 注册或登录获取token

#### 2.1.1 在`toutiao/resources/user/passport.py`中完善代码

> ```python
> ......
> class AuthorizationResource(Resource):
>     """
>     认证
>     """
>     def _generate_tokens(self, user_id, with_refresh_token=True):
>         """
>         生成token 和refresh_token
>         :param user_id: 用户id
>         :return: token, refresh_token
>         """
>         # 颁发JWT
>         # 过期时间 = 当前时间 + 2小时
>         # 'refresh': False 表示不是15天有效的token
>         exp = datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRY_HOURS'])
>         token = generate_jwt({'user_id': user_id, 'refresh': False},
>                              exp,
>                              current_app.config['JWT_SECRET'])
>         refresh_token = None
>         if with_refresh_token:
>             exp = datetime.utcnow() + timedelta(days=current_app.config['JWT_REFRESH_DAYS'])
>             refresh_token = generate_jwt({'user_id': user_id, 'refresh': True},
>                                          exp,
>                                          current_app.config['JWT_SECRET'])
>         return token, refresh_token
> 
>     def post(self):
>         """
>         登录创建token
>         """
> 		......
> ```

#### 2.1.2 测试代码

> 在`Test/test_f_01_jwt.py`中完成测试代码，进行测试：
>
> `set app:code:13161933309 123456`向主从redis中添加测试短信验证码
>
> ```python
> import requests, json
> 
> url = 'http://192.168.65.129:5000/v1_0/authorizations'
> 
> # code 向主从redis中手动添加短信验证码用于测试
> # redis-cli -p 6380/6381
> # set app:code:13161933309 123456
> # 关于app:code:13161933309是一个redis key，该key的命名方式在
> # 在toutiao/resources/user/passport.py的SMSVerificationCodeResource类的get函数
> data = {'mobile': '13161933309', 'code': '123456'}
> 
> # requests发送 POST raw application/json 请求
> resp = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
> 
> print(resp.json())
> ```

### 2.2 完成请求钩子

> 打开`toutiao/__init__.create_app`中关于`jwt_authentication`的注释
>
> 创建`common/utils/middlewares.py`，并完成代码
>
> ```python
> from flask import request, g
> from .jwt_util import verify_jwt # 导入从token中解析原始载荷的函数
> 
> # 在toutiao/__init__.py中的create_app函数中，配置了请求钩子
> # app.before_request(jwt_authentication)
> # 所以我们这里只需要完成jwt_authentication函数就好了
> def jwt_authentication():
>     """根据request.headers.Authorization中的jwt token验证用户身份
>     将token中user_id取出，放入g对象
>     将是否为refresh_token也记录在g对象中
>     方便每个请求在视图函数处理前，就能够在g对象中保存该用户的user_id，如果没有就为None"""
>     g.user_id = None # 每次请求开始都设置默认值
>     g.is_refresh_token = False # 每次请求开始都设置默认值
>     authorization = request.headers.get('Authorization')
>     # 如果request.headers.Authorization不是None
>     # 并且该值是以'Bearer '开头，就说明该请求带有token
>     if authorization and authorization.startswith('Bearer '):
>         token = authorization.strip()[7:] # strip()删除开头或是结尾的空格或换行符
>         payload = verify_jwt(token)
>         if payload:
>             g.user_id = payload.get('user_id')
>             g.is_refresh_token = payload.get('refresh')
> 
> ```

### 2.3 强制登录装饰器

> `common/utils/decorators.py`中专门存放各种装饰器，在其中添加下面的代码
>
> ```python
> def login_required(func):
>     """
>     用户必须登录装饰器
>     使用方法：放在method_decorators中
>     """
>     # Python装饰器（decorator）在实现的时候，被装饰后的函数其实已经是另外一个函数了（函数名等函数属性会发生改变）
>     # 为了不影响，Python的functools包中提供了一个叫wraps的decorator来消除这样的副作用。
>     @wraps(func)
>     def wrapper(*args, **kwargs):
>         if not g.user_id: # 如果g.user_id是None
>             return {'message': 'User must be authorized.'}, 401
>         elif g.is_refresh_token: # 如果是15天的token
>             return {'message': 'Do not use refresh token.'}, 403
>         else: # 存在g.user_id，且g.is_refresh_token为False
>             return func(*args, **kwargs)
>     return wrapper
> ```

### 2.4 更新token接口

#### 2.4.1 在`toutiao/resources/user/passport.py`中添加如下代码

> ```python
> class AuthorizationResource(Resource):
>     """
>     认证
>     """
>     ......
>     # 补充put函数，用于更新token
>     def put(self):
>         """刷新token
>         :return:  {message:OK, data:{token: 2小时有效token}}
>         """
>         # 如果存在user_id，并且是15天的refresh_token，说明需要刷新2小时有效token
>         if g.user_id is not None and g.is_refresh_token is not False:
>             # token, _ = ... 此时不需要refresh_token
>             token, _ = self._generate_tokens(g.user_id, with_refresh_token=False)
>             return {'token': token}, 201
>         else: # 返回403，通知客户端让用户重新登录
>             return {'message': 'Wrong refresh token.'}, 403
> ```

#### 2.4.2 测试代码

> ```python
> import requests, json
> 
> url = 'http://192.168.65.129:5000/v1_0/authorizations'
> 
> """测试 POST /v1_0/authorizations"""
> # code参数：需要向主从redis中手动添加短信验证码用于测试
> # redis-cli -p 6380/6381
> # set app:code:13161933309 123456
> # 关于app:code:13161933309是一个redis key，该key的命名方式在
> # 在toutiao/resources/user/passport.py的SMSVerificationCodeResource类的get函数
> # redis 通过哨兵集群操作主从
> REDIS_SENTINELS = [('127.0.0.1', '26380'),
>                    ('127.0.0.1', '26381'),
>                    ('127.0.0.1', '26382'),]
> REDIS_SENTINEL_SERVICE_NAME = 'mymaster'
> from redis.sentinel import Sentinel
> _sentinel = Sentinel(REDIS_SENTINELS)
> redis_master = _sentinel.master_for(REDIS_SENTINEL_SERVICE_NAME)
> # redis_slave = _sentinel.slave_for(REDIS_SENTINEL_SERVICE_NAME)
> redis_master.set('app:code:13161933309', '123456')
> 
> # 构造raw application/json形式的请求体
> data = json.dumps({'mobile': '13161933309', 'code': '123456'})
> # requests发送 POST raw application/json 请求
> resp = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
> print(resp.json())
> 
> """测试 PUT /v1_0/authorizations"""
> # 从上一个请求的响应中获取refresh_token
> refresh_token = resp.json()['data']['refresh_token']
> # 构造请求头：带着refresh_token发送请求python
> headers = {'Authorization': 'Bearer {}'.format(refresh_token)}
> resp = requests.put(url, headers=headers)
> print(resp.json()) # 打印获取的刷新的新token
> ```

### 2.5 本节实现需求的代码在toutiao项目中的应用工作流程

> ![jwt头条应用场景业务流程.png](../images/jwt头条应用场景业务流程.png)

