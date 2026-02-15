# 缓存理论：缓存数据

> 缓存数据以及缓存的数据结构的选择

[TOC]

<!-- toc -->

## 1. 缓存粒度

> 缓存粒度问题其实就是如何选择缓存数据的类型，要缓存什么东西

### 1.1 缓存数据类型介绍

> 在设计缓存的数据时，可以缓存以下类型的数据
>
> - 一个数值
> - 数据库记录
>   - 一组数据
>   - 联合查询的结果
> - 视图函数返回的结果
> - 页面

#### 1.1.1 一个数值

> 例如
>
> - 短信验证码
>
> - 用户状态
>
>   > 比如，用户状态是否可用：
>
>   - mysql数据库中`user_basic.status`
>
>   - reids中
>     - key `user:{user_id}: enable`
>     - value `1`or`0`

#### 1.1.2 数据库记录

> - 一条数据
>
>   > 以数据库一个数据对象的角度考虑， 应用更普遍
>   >
>   > 例如， 用户的扩展信息：
>   >
>   > - key：`user:{user_id}:profile`
>   > - value：json.dumps(UserProfile_dict)
>
>   ```python
>   user_profile = UserProfile.query.filter_by(id=1).first()
>   user_profile -> UserProfile
>   {
>       'user_id': '64',
>       'gender': '0',
>       'id_number': '210114198903096025',
>       'real_name': '武当山办事处王喇嘛'
>       ...
>   }  
>   ```
>
> - 一次数据库查询的结果
>
>   > 以数据库查询的角度考虑，应用场景较特殊，一般仅针对经常的复杂的联合查询结果进行缓存
>   >
>   > - 以sql语句hash结果作为key
>   > - 以查询结果作为value
>
>   ```python
>   query_result = User.query.join(User.profile).filter_by(id=1).first() 
>   -> sql = "select a.user_id, a.user_name, b.gender, b.birthday from tbl_user as a inner join tbl_profile as b on a.user_id=b.user_id where a.user_id=1;"
>   
>   # hash算法 md5
>   query = md5(sql)  # 'fwoifhwoiehfiowy23982f92h929y3209hf209fh2'
>   
>   # redis 写入数据并设置过期时间；使用的时候按sql取指纹 按指纹去redis取结果 没有结果再查库
>   setex(query, expiry, json.dumps(query_result))
>   ```

#### 1.1.3 一个视图的响应结果

> - key：url
> - value：json.dumps(view_func_results)
>
> ```python
> @route('/articles')
> @cache(exipry=30*60)
> def get_articles():
>     ch = request.args.get('ch')
>     articles = Article.query.all()
>     for article in articles:
>         user = User.query.filter_by(id=article.user_id).first()
>         comment = Comment.query.filter_by(article_id=article.id).all()
>   	results = {...} # 格式化输出
>     return results
>   
> # redis
> # '/artciels?ch=1':  json.dumps(results)
> ```

#### 1.1.4 一个页面

> - key：url
> - value：html
>
> ```python
> @route('/articles')
> @cache(exipry=30*60)
> def get_articles():
>     ch = request.args.get('ch')
>     articles = Article.query.all()
>     for article in articles:
>         user = User.query.filter_by(id=article.user_id).first()
>         comment = Comment.query.all()
>    results = {...}
>    return render_template('article_temp', results)
>   
> #  redis
> # '/artciels?ch=1':  html
> ```

### 1.2 项目中选择缓存数据类型

> - 要根据具体的业务实际情况来选择缓存数据的类型
>
> **touxiao项目中选择以数据库记录的级别作为缓存**

## 2. 缓存数据的保存方式

> 缓存数据所采用的数据结构

### 2.1 序列化字符串 json

> ```python
> # 序列化json字符：写入数据并设置过期时间
> # setex('user:{user_id}:info', 过期时间, value)
> setex('user:1:info', expiry, json.dumps(user_dict))
> ```
>
> - 优点
>   - 存储字符串节省空间
> - 缺点
>   - 序列化有时间开销
>   - 更新不方便（一般直接删除）

### 2.2 Redis的其他数据结构类型

> 早期Memcached只能选择把数据缓存为字符串，但redis还有其他的缓存方式，如hash、set、zset
>
> ```python
> hmset('user:1:info', user_dict) 
> ```
>
> - 优点
>   - 读写时不需要序列化转换
>   - 可以更新内部数据
> - 缺点
>   - 相比字符串，采用复合结构存储空间占用大





 