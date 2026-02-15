# JWT禁用问题

> 之前我们说过：`JWT的最大缺点是服务器不保存会话状态，所以在使用期间不可能取消令牌或更改令牌的权限。也就是说，一旦JWT签发，在有效期内将会一直有效。`
>
> 现在我们就来了解如何解决这个问题

[TOC]

<!-- toc -->

## 1. 需求

> token颁发给用户后，在有效期内服务端都会认可，但是如果在token的有效期内需要让token失效，该怎么办？
>
> 此问题的应用场景：
>
> - 用户修改密码，需要颁发新的token，禁用还在有效期内的老token
>   - 多端登录，一端改密码
> - 后台封禁用户

## 2. 思路 白名单策略

> - 保存特定用户的允许使用的新token，与该用户的请求对比
> - 保存的新token生存期长于旧token，只要保证新的比旧的后失效就ok

## 3. 解决方案

> > toutiao项目中尽采用短信验证码登录的方式，故没有jwt禁用的场景
>
> 在redis中使用set类型保存新生成的token
>
> ```python
> pl = redis_master.pipeline()
> pl.sadd(key, new_token)
> pl.expire(key, 10) # 10秒过期
> pl.execute()
> ```
>
> | 键                   | 类型 | 值      |
> | -------------------- | ---- | ------- |
> | user:{user_id}:token | set  | 新token |
>
> 客户端使用token进行请求时，如果验证token通过，则从redis中判断是否存在该用户的user:{}:token记录：
>
> - 若不存在记录，放行，进入视图进行业务处理
> - 若存在，则对比本次请求的token是否在redis保存的set中：
>   - 若存在，则放行
>   - 若不在set的数值中，则返回403状态码，不再处理业务逻辑
>
> ```python
> key = 'user:{}:token'.format(user_id)
> valid_tokens = redis_master.smembers(key) # 取出白名单集合
> if valid_tokens and old_token not in valid_tokens: # 如果白名单集合不为空，且token不在白名单集合中
>     print("{'message': 'Invalid token'}, 403")
> ```
>
> **注意**：
>
> 1. redis记录设置有效期的时长是一个token的有效期，保证旧token过期后，redis的记录也能自动清除，不占用空间。
> 2. 使用set保存新token的原因是，考虑到用户可能在旧token的有效期内，在其他多个设备进行了登录，需要生成多个新token，这些新token都要保存下来，既保证新token都能正常登录，又能保证旧token被禁用；`set`速度快。

## 4. 完整参考代码

> ```python
> REDIS_SENTINELS = [('127.0.0.1', '26380'),
>                    ('127.0.0.1', '26381'),
>                    ('127.0.0.1', '26382'),]
> REDIS_SENTINEL_SERVICE_NAME = 'mymaster'
> from redis.sentinel import Sentinel
> _sentinel = Sentinel(REDIS_SENTINELS)
> redis_master = _sentinel.master_for(REDIS_SENTINEL_SERVICE_NAME)
> 
> user_id = '13161933310'
> new_token = 'new_token_str'
> old_token = 'old_token_str'
> key = 'user:{}:token'.format(user_id) # 白名单集合
> 
> # 添加白名单
> pl = redis_master.pipeline()
> pl.sadd(key, new_token)
> pl.expire(key, 10) # 10秒
> pl.execute()
> 
> valid_tokens = redis_master.smembers(key) # 取出白名单集合
> if valid_tokens and old_token not in valid_tokens: # 如果白名单集合不为空，且token不在白名单集合中
>     print("{'message': 'Invalid token'}, 403")
> ```

