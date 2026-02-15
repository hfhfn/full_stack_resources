# 头条项目缓存实现

> 以原型图中 `个人页-用户信息` 为例

[TOC]

<!-- toc -->

## 1. 需求

> - 完成获取当前用户信息的接口，能够返回用户信息
>
> ![cache-个人信息需求.png](../images/cache-个人信息需求.png)

## 2. 需求分析

### 2.1 完成获取当前用户信息的接口 能够返回用户信息

> - GET /v1_0/user 
> - 需要加认证装饰器
> - 入参：无！
>   - 可以从g对象中获取user_id
> - 调用操作用户信息数据redis缓存及持久化工具类的函数，获取数据
> - 返回JSON
>   - 用户id
>   - 缓存的数据
>     - 用户昵称
>     - 头像
>     - 认证
>     - 简介
>   - 持久化存储的数据
>     - 发布
>     - 关注

### 2.2 完成操作用户信息数据redis缓存及持久化的工具类

#### 2.2.1 操作redis缓存数据的工具类

> > 需要对用户信息数据的缓存做哪些操作？
>
> - 查询
>   - 先查询redis缓存记录
>   - 如果有记录直接返回
>   - 如果没有记录，就查询数据库
>     - 如果数据库中有记录，就设置redis记录 string
>     - 如果数据库中没有记录，设置redis保存不存在的记录为 -1 防穿透
>   - 返回 字典 {手机号 昵称 头像 认证 简介}
> - 删除缓存
> - 判断是否存在
>   - 查询redis
>   - 如果存在redis记录
>     - 如果redis记录为-1，表示不存在 False
>     - 如果redis记录不为-1，表示用户存在 True
>   - 如果不存在redis记录
>     - 去数据库查询，判断是否存在
>       - 如果不存在，写redis记录为-1 False
>       - 如果存在，写redis记录 True

#### 2.2.2 操作redis持久化数据的工具类

> - 需要分别返回以下数据
>  - 发布
>   - 关注
> - 操作函数
>   - 获取
>   - 增加指定值，默认+1

### 2.3 要考虑关于缓存的哪些注意事项

> - 设置过期时间，注意时间，避免雪崩
> - 数据库中无记录，缓存设为固定值，避免穿透
> - 写入 ：先库后redis

### 2.4 要完成代码部分的逻辑位置

> 对比查看6.4章节的1.2小节

![6-7-1.png](../images/6-7-1.png)



## 3. 完成代码

> 在`common/cache/`下新建`user.py`

### 3.1 初步完成 操作用户信息缓存数据的工具类

> ```python
> class UserProfileCache():
>     """操作用户信息缓存数据的工具类"""
>     def __init__(self, user_id):
>         self.user_id = user_id
>         self.key = 'user:{}:profile'.format(user_id) # redis KEY
>         
>     def get(self):
>         """根据用户id查询缓存，返回用户信息"""
>         pass
>     
> 	def clear(self):
>         """根据用户id删除缓存"""
>         pass
> 
>     def exists(self):
>         """根据用户id判断用户是否存在"""
>         pass
> ```

### 3.2 初步完成根据用户id查询缓存 返回用户信息函数

> ```python
> from json import loads
> from flask import current_app
> from sqlalchemy.orm import load_only
> 
> from models.user import User
> 
> 
> class UserProfileCache():
>  """操作用户信息缓存数据的工具类"""
>  def __init__(self, user_id):
>      self.user_id = user_id
>      self.key = 'user:{}:profile'.format(user_id)
> 
>  def get(self):
>      """根据用户id查询缓存，返回用户信息
>      # 先查询redis缓存记录
>      # 如果有记录直接返回
>      # 如果没有记录，就查询数据库
>      # 如果数据库中没有记录，设置redis保存不存在的记录为 -1 防穿透
>      # 如果数据库中有记录，就设置redis记录 string
>      # 返回 字典 {手机号 昵称 头像 认证 简介}
>      :return: user dict
>      """
>      r = current_app.redis_cluster
>      # 先查询redis缓存记录
>      ret = r.get(self.key) # 返回bytes类型
>      # 如果有记录直接返回
>      if ret is not None:
>          if ret == b'-1': # '-1'表示数据库没有该记录
>              return None
>          # 这里是个坑！
>          ret = str(ret, encoding='utf-8').replace("'", '"').replace('None', '""')
>          print(ret)
>          return loads(ret) # json.loads/dumps 可以接收bytes类型
>      # 如果没有记录，就查询数据库
>      else:
>          user = User.query.options(load_only(
>              User.mobile,
>              User.name,
>              User.profile_photo,
>              User.introduction,
>              User.certificate
>          )).filter(User.id==self.user_id).first()
> 
>          # 如果数据库中没有记录，设置redis保存不存在的记录为 -1 防穿透
>          if user is None:
>              # 设置有效期 一会儿再说
>              r.setex(self.key, 有效期, '-1') 
>              return None
>          # 如果数据库中有记录，就设置redis记录 string
>          else:
>              user_dict = {
>                  'mobile': user.mobile,
>                  'name': user.name,
>                  'photo': user.profile_photo,
>                  'intro': user.introduction,
>                  'certi': user.certificate
>              }
>              # user_dict = dict(user)
>              # del user_dict['_sa_instance_state']
>              # 设置有效期 一会儿再说
>              r.setex(self.key, 有效期, user) 
>              # 返回 字典 {手机号 昵称 头像 认证 简介}
>              return user_dict
> 
> 
>  def clear(self):
>      """根据用户id删除缓存"""
>      pass
> 
>  def exists(self):
>      """根据用户id判断用户是否存在"""
>      pass
> ```

### 3.3 完成代码 缓存数据有效期函数

> - 创建`common/cache/constants.py`文件，完成缓存数据有效期函数
>
> ```python
> import random
> 
> 
> class BaseCacheTTL():
>     """缓存有效期，单位秒，要防止雪崩"""
>     TTL = 60 * 60 * 2 # 2小时 基础值
>     MAX_DELTA = 10 * 60 # 有效期上限
> 
>     # todo 改为类方法之后，可以不实例化就直接调用cls.func
>     @classmethod
>     def get_ttl(cls):
>         # 返回有效期时间范围内的随机值
>         return cls.TTL + random.randrange(0, cls.MAX_DELTA)
> 
> # todo 为防止缓存雪崩，在对不同的数据设置缓存有效期时采用设置不同有效期的方案，所以采用继承的方式
> 
> class UserProfileCacheTTL(BaseCacheTTL):
>     """用户信息缓存数据的有效期，单位秒"""
>     pass
> 
> # todo 对于不存在的用户，缓存有效期稍微短一些
> class UserNotExistCacheTTL(BaseCacheTTL):
>     TTL = 60 * 5
>     MAX_DELTA = 60 * 10
> ```
>
> - 修改`common/cache/user.py`中的 `UserProfileCache.get`函数
>
> ```python
> ...
> from common.cache import constants    
>     ...
>     # 设置数据库无数据的有效期
>     r.setex(self.key, constants.UserNotExistCacheTTL.get_ttl(), '-1') 
>     ...
>     # 设置有效期      
>     r.setex(self.key, constants.UserProfileCacheTTL.get_ttl(), user_dict) # 设置有效期
> 	...
> ```

### 3.4 完善 查缓存返用户信息的函数

> - 捕获redis异常
>   - `redis.exceptions.RedisError`
> - 捕获并抛出`DatabaseError`
>   - `from sqlalchemy.exc.DatabaseError` 
> - `current_app.logger.error`记录flask的异常日志
>
> > `common/cache/user.py`
>
> ```python
> ...
> from redis.exceptions import RedisError
> from sqlalchemy.exc import DatabaseError
> 	...
>  def get(self):
>      """根据用户id查询缓存，返回用户信息
>      # 先查询redis缓存记录
>      # 如果有记录直接返回
>      # 如果没有记录，就查询数据库
>          # 如果数据库中没有记录，设置redis保存不存在的记录为 -1 防穿透
>          # 如果数据库中有记录，就设置redis记录 string
>      # 返回 字典 {手机号 昵称 头像 认证 简介}
>      :return: user dict or None
>      """
>      r = current_app.redis_cluster
> 
>      # 先查询redis缓存记录
>      try:
>          ret = r.get(self.key) # 返回bytes类型
>      except RedisError as e:
>          current_app.logger.error(e)
>          # 在redis查缓存出现异常时，还可以继续向下执行，去查库，最终返回
>          ret = None # 所以设为 ret = None
> 
>      # 如果有记录直接返回
>      if ret is not None:
>          if ret == b'-1': # '-1'表示数据库没有该记录
>              return None
>          # 这里是个坑！
>          ret = str(ret, encoding='utf-8').replace("'", '"').replace('None', '""')
>          print(ret)
>          return loads(ret) # json.loads/dumps 可以接收bytes类型
>      # 如果没有记录，就查询数据库
>      else:
>          try:
>              user = User.query.options(load_only(
>                  User.mobile,
>                  User.name,
>                  User.profile_photo,
>                  User.introduction,
>                  User.certificate
>              )).filter(User.id==self.user_id).first()
>          except DatabaseError as e:
>              current_app.logger.error(e)
>              raise e # 抛出异常，不能None
>              # 如果return None会和"数据库中没有记录"产生歧义
> 
>          # 如果数据库中没有记录，设置redis保存不存在的记录为 -1 防穿透
>          if user is None:
>              try: # 一旦写缓存异常，并不影响下一次写入缓存
>                  r.setex(self.key, constants.UserNotExistCacheTTL.get_ttl(), '-1') # 设置有效期
>              except RedisError as e:
>                  current_app.logger.error(e)
>              return None
>          # 如果数据库中有记录，就设置redis记录 string
>          else:
>              user_dict = {
>                  'mobile': user.mobile,
>                  'name': user.name,
>                  'photo': user.profile_photo,
>                  'intro': user.introduction,
>                  'certi': user.certificate
>              }
>              # user_dict = dict(user)
>              # del user_dict['_sa_instance_state']
>              try: # 一旦写缓存异常，并不影响下一次写入缓存
>                  r.setex(self.key, constants.UserProfileCacheTTL.get_ttl(), user_dict) # 设置有效期
>              except RedisError as e:
>                  current_app.logger.error(e)
> 
>              # 返回 字典 {手机号 昵称 头像 认证 简介}
>              return user_dict
> ...            
> ```

### 3.5 完成删除缓存函数

> `common/cache/user.py`
>
> ```python
> ...
>     def clear(self):
>         """根据用户id删除缓存"""
>         try:
>             r = current_app.redis_cluster
>             r.delete(self.key)
>         except RedisError as e:
>             # 删除失败还有过期时间呢！不要怕
>             current_app.logger.error(e)
> ...
> ```

### 3.6 完成判断用户是否存在函数

> `common/cache/user.py`
>
> ```python
>     ...
>     def exists(self):
>         """根据用户id判断用户是否存在
>         # 查询redis
>         # 如果存在redis记录
>             # 如果redis记录为-1，表示不存在 False
>             # 如果redis记录不为-1，表示用户存在 True
>         # 如果不存在redis记录
>             # 去数据库查询，判断是否存在
>                 # 如果不存在，写redis记录为-1 False
>                 # 如果存在，写redis记录 True
>         """
>         r = current_app.redis_cluster
>         # 查询redis
>         try:
>             ret = r.get(self.key)
>         except RedisError as e:
>             current_app.logger.error(e)
>             raise e # 一旦出现异常，无法判断用户是否存在，所以抛出异常
> 
>         # 如果存在redis记录
>         if ret is not None:
>             # 如果redis记录为-1，表示不存在 False
>             if ret == b'-1':
>                 return False
>             # 如果redis记录不为-1，表示用户存在 True
>             else:
>                 return True
>         # 如果不存在redis记录
>         else:
>             # 去数据库查询，判断是否存在
>                 # 如果不存在，写redis记录为-1 False
>                 # 如果存在，写redis记录 True
>             def query_db():
>                 """查询数据库，从self.get()函数中节选复制
>                 如果不存在，写redis缓存为-1 return None
>                 如果存在，写redis缓存 return user_dict
>                 """
>                 try:
>                     user = User.query.options(load_only(
>                         User.mobile,
>                         User.name,
>                         User.profile_photo,
>                         User.introduction,
>                         User.certificate
>                     )).filter(User.id==self.user_id).first()
>                 except DatabaseError as e:
>                     current_app.logger.error(e)
>                     raise e # 抛出异常，不能None
>                     # 如果return None会和"数据库中没有记录"产生歧义
> 
>                 # 如果数据库中没有记录，设置redis保存不存在的记录为 -1 防穿透
>                 if user is None:
>                     try: # 一旦写缓存异常，并不影响下一次写入缓存
>                         r.setex(self.key, constants.UserNotExistCacheTTL.get_ttl(), '-1') # 设置有效期
>                     except RedisError as e:
>                         current_app.logger.error(e)
>                     return None
>                 # 如果数据库中有记录，就设置redis记录 string
>                 else:
>                     user_dict = {
>                         'mobile': user.mobile,
>                         'name': user.name,
>                         'photo': user.profile_photo,
>                         'intro': user.introduction,
>                         'certi': user.certificate
>                     }
>                     # user_dict = dict(user)
>                     # del user_dict['_sa_instance_state']
>                     try: # 一旦写缓存异常，并不影响下一次写入缓存
>                         r.setex(self.key, constants.UserProfileCacheTTL.get_ttl(), user_dict) # 设置有效期
>                     except RedisError as e:
>                         current_app.logger.error(e)
> 
>                     # 返回 字典 {手机号 昵称 头像 认证 简介}
>                     return user_dict
> 
>             db_ret = query_db()
>             if db_ret is None:
>                 return False
>             else:
>                 return True
> ```

### 3.7 抽象出查库保存数据到缓存的函数

> `common/cache/user.py`

> ```python
>     ...
>     def query_db(self):
>         """查询数据库，从self.get()函数中节选复制
>         如果不存在，写redis缓存为-1 return None
>         如果存在，写redis缓存 return user_dict or None
>         """
>         r = current_app.redis_cluster
>         try:
>             user = User.query.options(load_only(
>                 User.mobile,
>                 User.name,
>                 User.profile_photo,
>                 User.introduction,
>                 User.certificate
>             )).filter(User.id == self.user_id).first()
>         except DatabaseError as e:
>             current_app.logger.error(e)
>             raise e  # 抛出异常，不能None
>             # 如果return None会和"数据库中没有记录"产生歧义
> 
>         # 如果数据库中没有记录，设置redis保存不存在的记录为 -1 防穿透
>         if user is None:
>             try:  # 一旦写缓存异常，并不影响下一次写入缓存
>                 r.setex(self.key, constants.UserNotExistCacheTTL.get_ttl(), '-1')  # 设置有效期
>             except RedisError as e:
>                 current_app.logger.error(e)
>             return None
>         # 如果数据库中有记录，就设置redis记录 string
>         else:
>             user_dict = {
>                 'mobile': user.mobile,
>                 'name': user.name,
>                 'photo': user.profile_photo,
>                 'intro': user.introduction,
>                 'certi': user.certificate
>             }
>             # user_dict = dict(user)
>             # del user_dict['_sa_instance_state']
>             try:  # 一旦写缓存异常，并不影响下一次写入缓存
>                 r.setex(self.key, constants.UserProfileCacheTTL.get_ttl(), user_dict)  # 设置有效期
>             except RedisError as e:
>                 current_app.logger.error(e)
> 
>             # 返回 字典 {手机号 昵称 头像 认证 简介}
>             return user_dict
> 
>     def get(self):
>         """根据用户id查询缓存，返回用户信息
>         # 先查询redis缓存记录
>         # 如果有记录直接返回
>         # 如果没有记录，就查询数据库
>             # 如果数据库中没有记录，设置redis保存不存在的记录为 -1 防穿透
>             # 如果数据库中有记录，就设置redis记录 string
>         # 返回 字典 {手机号 昵称 头像 认证 简介}
>         :return: user dict or None
>         """
>         r = current_app.redis_cluster
> 
>         # 先查询redis缓存记录
>         try:
>             ret = r.get(self.key) # 返回bytes类型
>         except RedisError as e:
>             current_app.logger.error(e)
>             # 在redis查缓存出现异常时，还可以继续向下执行，去查库，最终返回
>             ret = None # 所以设为 ret = None
> 
>         # 如果有记录直接返回
>         if ret is not None:
>             if ret == b'-1': # '-1'表示数据库没有该记录
>                 return None
>             return loads(ret) # json.loads/dumps 可以接收bytes类型
>         else:
>             # 如果没有记录，就查询数据库
>                 # 如果数据库中没有记录，设置redis保存不存在的记录为 -1 防穿透
>                 # 如果数据库中有记录，就设置redis记录 string
>                     # 返回 字典 {手机号 昵称 头像 认证 简介}
>             user_dict = self.query_db()
>             return user_dict
> 
>     def clear(self):
>         """根据用户id删除缓存"""
>         r = current_app.redis_cluster
>         try:
>             r.delete(self.key)
>         except RedisError as e:
>             # 删除失败还有过期时间呢！不要怕
>             current_app.logger.error(e)
> 
>     def exists(self):
>         """根据用户id判断用户是否存在
>         # 查询redis
>         # 如果存在redis记录
>             # 如果redis记录为-1，表示不存在 False
>             # 如果redis记录不为-1，表示用户存在 True
>         # 如果不存在redis记录
>             # 去数据库查询，判断是否存在
>                 # 如果不存在，写redis记录为-1 False
>                 # 如果存在，写redis记录 True
>         """
>         r = current_app.redis_cluster
>         # 查询redis
>         try:
>             ret = r.get(self.key)
>         except RedisError as e:
>             current_app.logger.error(e)
>             raise e # 一旦出现异常，无法判断用户是否存在，所以抛出异常
> 
>         # 如果存在redis记录
>         if ret is not None:
>             # 如果redis记录为-1，表示不存在 False
>             if ret == b'-1':
>                 return False
>             # 如果redis记录不为-1，表示用户存在 True
>             else:
>                 return True
>         # 如果不存在redis记录
>         else:
>             # 去数据库查询，判断是否存在
>                 # 如果不存在，写redis记录为-1 False
>                 # 如果存在，写redis记录 True
>             user_dict = self.query_db()
>             if user_dict is None:
>                 return False
>             else:
>                 return True
> ```

### 3.8 完成返回用户个人信息的接口

#### 3.8.1 注册路由

> 在`toutiao/resources/user/__init__.py`中注册路由
>
> ```python
> user_api.add_resource(profile.CurrentUserResource, '/v1_0/user',
>                       endpoint='CurrentUser')
> ```

#### 3.8.2 完成接口代码

> 在`toutiao/resources/user/profile.py`中，完成 `CurrentUserResource`视图类代码
>
> ```python
> ......
> class CurrentUserResource(Resource):
>     """返回用户信息接口"""
>     method_decorators = [login_required] # 用户认证装饰器
> 
>     def get(self):
>         # 调用操作用户信息数据redis缓存及持久化工具类的函数，获取数据
>         user_dict = UserProfileCache(g.user_id).query_db()
>         user_dict['user_id'] = g.user_id
>         user_dict['arts_count'] = 0 # 没有实现，先拿0代替
>         user_dict['following_count'] = 0
>         return user_dict
>    ```

#### 3.8.3 测试接口

> `Test/test_f_cache/test_f_cache_1.py`
>
> ```python
> import requests, json
> 
> """测试 POST /v1_0/authorizations 登录请求"""
> # code参数：需要向主从redis中手动添加短信验证码用于测试
> # redis-cli -p 6380/6381
> # set app:code:13161933309 123456
> # 关于app:code:13161933309是一个redis key，该key的命名方式在
> # 在toutiao/resources/user/passport.py的SMSVerificationCodeResource类的get函数
> # redis 通过哨兵集群操作主从
> 
> REDIS_SENTINELS = [('127.0.0.1', '26380'),
>                 ('127.0.0.1', '26381'),
>                 ('127.0.0.1', '26382'),]
>    REDIS_SENTINEL_SERVICE_NAME = 'mymaster'
>    from redis.sentinel import Sentinel
> _sentinel = Sentinel(REDIS_SENTINELS)
> redis_master = _sentinel.master_for(REDIS_SENTINEL_SERVICE_NAME)
> # redis_slave = _sentinel.slave_for(REDIS_SENTINEL_SERVICE_NAME)
> redis_master.set('app:code:18911111111', '123456')
> 
> """登录"""
> # 构造raw application/json形式的请求体
> data = json.dumps({'mobile': '18911111111', 'code': '123456'})
> # requests发送 POST raw application/json 登录请求
> url = 'http://192.168.65.131:5000/v1_0/authorizations'
> resp = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
> print(resp.json())
> 
> """测试 get /v1_0/user"""
> # 从登录请求的响应中获取token
> token = resp.json()['data']['token']
> print(token)
> 
> # token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjU3ODkzNjUsInVzZXJfaWQiOjExNTk1MjAzMzE1MjI2Mzc4MzUsInJlZnJlc2giOmZhbHNlfQ.0P1YpOQi5BwsHn46Ayv5HVWojJ54XdSCxd4FqB6aKHE'
> 
> # 构造请求头：带着refresh_token发送请求
> headers = {'Authorization': 'Bearer {}'.format(token)}
> url = 'http://192.168.65.131:5000/v1_0/user'
> resp = requests.get(url, headers=headers)
> print(resp.json()) # 打印获取的刷新的新token
> ```
> 
> - 也可以通过``进入redis cluster集群中查看缓存的用户数据
>
> ```shell
>redis-cli -c -p 7000
>   keys *
>   get user:user_id:profile
>   ```
>   
>   - 测试缓存功能
>
> - 通过测试后git提交代码



## 4. 本章节完整参考代码

- `common/cache/user.py`

```python
from json import loads
from flask import current_app
from sqlalchemy.orm import load_only
from redis.exceptions import RedisError
from sqlalchemy.exc import DatabaseError

from models.user import User
from common.cache import constants


class UserProfileCache():
    """操作用户信息缓存数据的工具类"""
    def __init__(self, user_id):
        self.user_id = user_id
        self.key = 'user:{}:profile'.format(user_id)

    def query_db(self):
        """查询数据库，从self.get()函数中节选复制
        如果不存在，写redis缓存为-1 return None
        如果存在，写redis缓存 return user_dict or None
        """
        r = current_app.redis_cluster
        try:
            user = User.query.options(load_only(
                User.mobile,
                User.name,
                User.profile_photo,
                User.introduction,
                User.certificate
            )).filter(User.id == self.user_id).first()
        except DatabaseError as e:
            current_app.logger.error(e)
            raise e  # 抛出异常，不能None
            # 如果return None会和"数据库中没有记录"产生歧义

        # 如果数据库中没有记录，设置redis保存不存在的记录为 -1 防穿透
        if user is None:
            try:  # 一旦写缓存异常，并不影响下一次写入缓存
                r.setex(self.key, constants.UserNotExistCacheTTL.get_ttl(), '-1')  # 设置有效期
            except RedisError as e:
                current_app.logger.error(e)
            return None
        # 如果数据库中有记录，就设置redis记录 string
        else:
            user_dict = {
                'mobile': user.mobile,
                'name': user.name,
                'photo': user.profile_photo,
                'intro': user.introduction,
                'certi': user.certificate
            }
            # user_dict = dict(user)
            # del user_dict['_sa_instance_state']
            try:  # 一旦写缓存异常，并不影响下一次写入缓存
                r.setex(self.key, constants.UserProfileCacheTTL.get_ttl(), user_dict)  # 设置有效期
            except RedisError as e:
                current_app.logger.error(e)

            # 返回 字典 {手机号 昵称 头像 认证 简介}
            return user_dict

    def get(self):
        """根据用户id查询缓存，返回用户信息
        # 先查询redis缓存记录
        # 如果有记录直接返回
        # 如果没有记录，就查询数据库
            # 如果数据库中没有记录，设置redis保存不存在的记录为 -1 防穿透
            # 如果数据库中有记录，就设置redis记录 string
        # 返回 字典 {手机号 昵称 头像 认证 简介}
        :return: user dict or None
        """
        r = current_app.redis_cluster

        # 先查询redis缓存记录
        try:
            ret = r.get(self.key) # 返回bytes类型
        except RedisError as e:
            current_app.logger.error(e)
            # 在redis查缓存出现异常时，还可以继续向下执行，去查库，最终返回
            ret = None # 所以设为 ret = None

        # 如果有记录直接返回
        if ret is not None:
            if ret == b'-1': # '-1'表示数据库没有该记录
                return None
            return loads(ret) # json.loads/dumps 可以接收bytes类型
        else:
            # 如果没有记录，就查询数据库
                # 如果数据库中没有记录，设置redis保存不存在的记录为 -1 防穿透
                # 如果数据库中有记录，就设置redis记录 string
                    # 返回 字典 {手机号 昵称 头像 认证 简介}
            user_dict = self.query_db()
            return user_dict

    def clear(self):
        """根据用户id删除缓存"""
        r = current_app.redis_cluster
        try:
            r.delete(self.key)
        except RedisError as e:
            # 删除失败还有过期时间呢！不要怕
            current_app.logger.error(e)

    def exists(self):
        """根据用户id判断用户是否存在
        # 查询redis
        # 如果存在redis记录
            # 如果redis记录为-1，表示不存在 False
            # 如果redis记录不为-1，表示用户存在 True
        # 如果不存在redis记录
            # 去数据库查询，判断是否存在
                # 如果不存在，写redis记录为-1 False
                # 如果存在，写redis记录 True
        """
        r = current_app.redis_cluster
        # 查询redis
        try:
            ret = r.get(self.key)
        except RedisError as e:
            current_app.logger.error(e)
            raise e # 一旦出现异常，无法判断用户是否存在，所以抛出异常

        # 如果存在redis记录
        if ret is not None:
            # 如果redis记录为-1，表示不存在 False
            if ret == b'-1':
                return False
            # 如果redis记录不为-1，表示用户存在 True
            else:
                return True
        # 如果不存在redis记录
        else:
            # 去数据库查询，判断是否存在
                # 如果不存在，写redis记录为-1 False
                # 如果存在，写redis记录 True
            user_dict = self.query_db()
            if user_dict is None:
                return False
            else:
                return True
```

- `common/cache/constants.py`

```python
import random


class BaseCacheTTL():
    """缓存有效期，单位秒，要防止雪崩"""
    TTL = 60 * 60 * 2 # 2小时 基础值
    MAX_DELTA = 10 * 60 # 有效期上限

    # todo 改为类方法之后，可以不实例化就直接调用cls.func
    @classmethod
    def get_ttl(cls):
        # 返回有效期时间范围内的随机值
        return cls.TTL + random.randrange(0, cls.MAX_DELTA)

# todo 为防止缓存雪崩，在对不同的数据设置缓存有效期时采用设置不同有效期的方案，所以采用继承的方式

class UserProfileCacheTTL(BaseCacheTTL):
    """用户信息缓存数据的有效期，单位秒"""
    pass

# todo 对于不存在的用户，缓存有效期稍微短一些
class UserNotExistCacheTTL(BaseCacheTTL):
    TTL = 60 * 5
    MAX_DELTA = 60 * 10


```

- `toutiao/resources/user/__init__.py`

```python
......
user_api.add_resource(profile.CurrentUserResource, '/v1_0/user',
                      endpoint='CurrentUser')
......
```

- `toutiao/resources/user/profile.py`

```python
...
class CurrentUserResource(Resource):
    """返回用户信息接口"""
    method_decorators = [login_required] # 用户认证装饰器

    def get(self):
        # 调用操作用户信息数据redis缓存及持久化工具类的函数，获取数据
        user_dict = UserProfileCache(g.user_id).query_db()
        user_dict['user_id'] = g.user_id
        user_dict['arts_count'] = 0
        user_dict['following_count'] = 0
        return user_dict
```

- `Test/test_f_cache/test_f_cache_1.py`

```python
import requests, json

"""测试 POST /v1_0/authorizations 登录请求"""
# code参数：需要向主从redis中手动添加短信验证码用于测试
# redis-cli -p 6380/6381
# set app:code:13161933309 123456
# 关于app:code:13161933309是一个redis key，该key的命名方式在
# 在toutiao/resources/user/passport.py的SMSVerificationCodeResource类的get函数
# redis 通过哨兵集群操作主从

REDIS_SENTINELS = [('127.0.0.1', '26380'),
                   ('127.0.0.1', '26381'),
                   ('127.0.0.1', '26382'),]
REDIS_SENTINEL_SERVICE_NAME = 'mymaster'
from redis.sentinel import Sentinel
_sentinel = Sentinel(REDIS_SENTINELS)
redis_master = _sentinel.master_for(REDIS_SENTINEL_SERVICE_NAME)
# redis_slave = _sentinel.slave_for(REDIS_SENTINEL_SERVICE_NAME)
redis_master.set('app:code:18911111111', '123456')

"""登录"""
# 构造raw application/json形式的请求体
data = json.dumps({'mobile': '18911111111', 'code': '123456'})
# requests发送 POST raw application/json 登录请求
url = 'http://192.168.65.131:5000/v1_0/authorizations'
resp = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
print(resp.json())

"""测试 get /v1_0/user"""
# 从登录请求的响应中获取token
token = resp.json()['data']['token']
print(token)

# token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NjU3ODk3MDcsInVzZXJfaWQiOjExNTk1MjAzMzE1MjI2Mzc4MzUsInJlZnJlc2giOmZhbHNlfQ.qiwaawtwruoQS7JaXupUMhh48nt46ZVai7DDqt5MvwM'
# 构造请求头：带着refresh_token发送请求
headers = {'Authorization': 'Bearer {}'.format(token)}
url = 'http://192.168.65.131:5000/v1_0/user'
resp = requests.get(url, headers=headers)
print(resp.json()) # 打印获取的刷新的新token
```



## 5. 关于json模块操作bytes类型和json字符串的坑

```python
ret = b"{'a': None}" 
# print(json.loads(ret)) # 抛出异常
ret = str(ret, encoding='utf-8').replace("'", '"').replace('None', '""')
print(ret)
print(json.loads(ret))
```







