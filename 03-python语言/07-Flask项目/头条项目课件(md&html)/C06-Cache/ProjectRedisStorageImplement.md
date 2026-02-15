# 项目Redis持久存储工具类实现

> 这一章节来完成redis持久存储工具类的代码，以`用户文章总数`和`用户关注总数`为例

[TOC]

<!-- toc -->

## 1. 分析

> 以`用户文章总数`和`用户关注总数`为例，完成redis持久存储工具类的代码
>
> - 函数
>   - 获取
>   - 增加指定值，默认+1
> - 分别封装
>   - 发布总数 工具类
>   - 关注总数 工具类
> - 因为是持久化存储，所以使用redis主从数据库

## 2. 完成代码

### 2.1 完成发布总数工具类

> `common/cache/statistic.py`
>
> ```python
> from flask import current_app
> 
> 
> class UserArticleCountStorage():
> 
>  def __init__(self, user_id):
>      self.user_id = user_id
>      self.key = 'count:user:arts'
> 
>  def get(self):
>      # 根据user_id取该用户的xx总数
>      # user_id是zset的值，唯一；分数可以有重复
>      # 其实就是 根据zset的 value 获取 score
>      # zscore(key, value) ==> score
>      ret = current_app.redis_master.zscore(self.key, self.user_id)
> 
>      if ret is None:
>          return 0
>      else:
>          return int(ret)
> 
>  def incr(self, n=1):
>      # 对制定用户发布总数 + 1
>      # 其实就是 对zset 根据key的value 让score+1
>      # zincrby(key, value, 1) ==> score+1
>      current_app.redis_master.zincrby(self.key, self.user_id, n)
> ```

### 2.2 完成关注总数工具类

> `common/cache/statistic.py`
>
> ```python
> ...
> class UserFollowingCountStorage():
> 
>  def __init__(self, user_id):
>      self.user_id = user_id
>      self.key = 'count:user:following'
> 
>  def get(self):
>      # 根据user_id取该用户的xx总数
>      # user_id是zset的值，唯一；分数可以有重复
>      # 其实就是 根据zset的 value 获取 score
>      # zscore(key, value) ==> score
>      ret = current_app.redis_master.zscore(self.key, self.user_id)
> 
>      if ret is None:
>          return 0
>      else:
>          return int(ret)
> 
>  def incr(self, n=1):
>      # 对指定用户关注总数 + 1
>      # 其实就是 对zset 根据key的value 让score+1
>      # zincrby(key, value, 1) ==> score+1
>      current_app.redis_master.zincrby(self.key, self.user_id, n)
> ```
>
> - 只更改了 `类名` 和 `redis key`

### 2.3 封装代码

> 在完成上述代码后发现：两个类只有 `类名` 和 `redis key`不同
>
> `common/cache/statistic.py`
>
> ```python
> from flask import current_app
> 
> class BaseCountStorage():
>  key = ''
> 
>  def __init__(self, user_id):
>      self.user_id = user_id
> 
>  def get(self):
>      # 根据user_id取该用户的xx总数
>      # user_id是zset的值，唯一；分数可以有重复
>      # 其实就是 根据zset的 value 获取 score
>      # zscore(key, value) ==> score
>      ret = current_app.redis_master.zscore(self.key, self.user_id)
> 
>      if ret is None:
>          return 0
>      else:
>          return int(ret)
> 
>  def incr(self, n=1):
>      # 对制定用户xx总数 + 1
>      # 其实就是 对zset 根据key的value 让score+1
>      # zincrby(key, value, 1) ==> score+1
>      current_app.redis_master.zincrby(self.key, self.user_id, n)
> 
> class UserArticleCountStorage(BaseCountStorage):
>  """用户发布总数工具类"""
>  key = 'count:user:arts'
> 
> 
> class UserFollowingCountStorage(BaseCountStorage):
>  """用户关注总数工具类"""
>  key = 'count:user:following'
> ```

### 2.4 完善代码

> > - 可以把`BaseCountStorage`类的函数声明为类方法，这样就可以直接调用，无需实例化
> > - 要考虑redis master连接失败，就使用redis slaver操作
> >   - `redis.exceptions.ConnectionError`
>
> `common/cache/statistic.py`
>
> ```python
> from flask import current_app
> from redis.exceptions import ConnectionError
> 
> 
> class BaseCountStorage():
>  key = ''
> 
>  @classmethod
>  def get(cls, user_id):
>      """
>      # 根据user_id取该用户的xx总数
>      # user_id是zset的值，唯一；分数可以有重复
>      # 其实就是 根据zset的 value 获取 score
>      # zscore(key, value) ==> score
>      :param user_id:
>      :return: int
>      """
>      try: # redis master连接失败，就使用redis slaver操作
>          ret = current_app.redis_master.zscore(cls.key, user_id)
>      except ConnectionError as e:
>          current_app.logger.error(e)
>          ret = current_app.redis_slave.zscore(cls.key, user_id)
> 
>      if ret is None:
>          return 0
>      else:
>          return int(ret)
> 
>  @classmethod
>  def incr(cls, user_id, n=1):
>      """
>      # 对制定用户xx总数 + 1
>      # 其实就是 对zset 根据key的value 让score+1
>      # zincrby(key, value, 1) ==> score+1
>      :param user_id:
>      :param n:
>      :return:
>      """
>      try: # redis master连接失败，就使用redis slaver操作
>          current_app.redis_master.zincrby(cls.key, user_id, n)
>      except ConnectionError as e:
>          current_app.logger.error(e)
>          current_app.redis_slave.zincrby(cls.key, user_id, n)
> 
> 
> class UserArticleCountStorage(BaseCountStorage):
>  """用户发布总数工具类"""
>  key = 'count:user:arts'
> 
> 
> class UserFollowingCountStorage(BaseCountStorage):
>  """用户关注总数工具类"""
>  key = 'count:user:following'
> ```

