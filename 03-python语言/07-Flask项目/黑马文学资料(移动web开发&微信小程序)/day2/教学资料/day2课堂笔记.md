### 1.JWT：json web token

* 概念：字符串；
* 作用：实现状态保持的一种方案，cookie和session；
* JWT token：服务器不保存，
  * header：头，存储基本的加密算法。
  * payload：载荷，存储业务数据，比如用户id，expire过期时间。
  * signature：签名，确保信息不会被修改。
  * token = header  + payload + signature

### 2.jwt工具的封装

* 安装pyjwt模块

* 在lib目录下，封装jwt_utils.py封装工具代码

* ```
  # jwt工具的封装
  # 步骤：
  # 1.导入jwt模块
  # 2.封装jwt生成的函数，必须要有密钥secret_key
  	# 返回token
  # 3.封装jwt校验的函数
  	# 返回payload
  ```

### 3.用户登录

* 登录接口的实现步骤：
  * 1、获取参数code
  * 2、获取参数iv、envryptedData
  * 3、调用微信工具，获取session_key
  * 4、根据session_key，调用微信工具，获取用户信息
  * 5、判断是否获取到openID
  * 6、保存用户数据
    * 查询mysql数据库，判断openID是否存在
    * 如果openID不存在，保存用户信息
    * 否则，更新用户信息
  * 7、调用jwt工具，生成token
  * 8、返回数据

* 封装工具，生成token的有效期

  * 有效期：24小时；
  * 当前时间：datetime获取当前时间，时间差操作timedelta

  * 总结：

  * ```
    1、生成当前时间
    2、根据时间差，指定token的过期时间,
    3、调用jwt工具，传入过期时间
    4、返回token
    ```

### 4.用户权限校验

* 需求：在每次请求前，校验用户的身份信息，从token中提取用户id
* 使用请求钩子实现，在每次请求前都会执行，@app.before_request
* g对象：应用上下文对象，在请求过程中可以临时存储数据。
* 实现步骤：
  * 1.封装工具，/lib/middlewrares.py
  * 2.定义函数，获取用户头信息，Authorization
  * 3.从payload中提取用户id，把用户id赋值给g对象

### 5.登录验证装饰器

* 需求：取出用户信息后，判断用户是否登录，如果登录后，可以进入视图，否则不允许进入视图。
* 实现步骤：
  * 1、封装工具，/lib/decoraters.py
  * 2、定义装饰器
  * 3、判断用户id是否存在，从g对象中尝试获取用户id
  * 4、返回结果









