# SQLAlchemy操作

> 本章节就以上一小节中完成的toutiao项目中`user_basic`、`user_profile`、 `user_relation`三个表及其模型类最为演示案例

[TOC]

<!-- toc -->

## 1 新增

### 1.1 增加一条数据

```python
user = User(mobile='15612345678', name='itcast')
db.session.add(user)
db.session.commit()
profile = Profile(id=user.id)
db.session.add(profile)
db.session.commit()
```

### 1.2 批量添加多条数据

```python
db.session.add_all([user1, user2, user3])
db.session.commit()
```

### 1.3 完整参考代码

> `Test/test_sqlalchemy/02.py`

```python
from datetime import datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/toutiao' # 数据库连接地址
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据库修改, 开启后影响性能
    SQLALCHEMY_ECHO = True # 开启后, 可以在控制台打印底层执行的sql语句
app.config.from_object(Config)
app.config['JSON_AS_ASCII'] = False # jsonify返回的值禁用ascii编码：utf8
# 创建数据库连接对象
db = SQLAlchemy(app)

class User(db.Model):
    ......   
class UserProfile(db.Model):
	......
class Relation(db.Model):
	......

@app.route('/')
def index():
    # 返回所有路由
    rules_iterator = app.url_map.iter_rules()
    return jsonify({rule.endpoint: rule.rule for rule in rules_iterator if rule.endpoint not in ('route_map', 'static')})

@app.route('/add')
def add_data():
    """增加数据"""
    user = User(mobile='13161933310', name='金馆长1') # 创建/实例化数据对象
    db.session.add(user) # 将数据对象添加到链接对象的session（会话）中
    db.session.commit() # 提交会话 此时add(user)写入数据才生效
    profile = UserProfile(id=user.id) # 先把user写入数据库后，user_basic表中才能有这个id
    db.session.add(profile)
    db.session.commit()

    # 同时写入多条数据
    # user1 = User(mobile='13911224611', name='金馆长4')
    # user2 = User(mobile='13911224612', name='金馆长5')
    # user3 = User(mobile='13911224613', name='金馆长6')
    # db.session.add_all([user1, user2, user3])
    # db.session.commit()

    return "add_data"

if __name__ == '__main__':
    app.run(debug=True)
```



## 2 查询

> sqlalchemy的查询函数和原生sql的查询语句有很多相似的地方，比如原生sql的`group by`分组，对应的就是`group_by()`函数，篇幅有限不能全部举例展示

### 2.1 基础查询

#### 2.1.1 all() 

- 查询所有，返回列表

```python
User.query.all()
```

- 参考代码

```python
@app.route('/get_all')
def get_all():
    # 查询所有 User.query.all()
    users = User.query.all() # 返回由数据对象构成的列表
    # print(users)
    ret_dict = {}
    for user in users:
        print(user.name, user.mobile)
        ret_dict[user.mobile] = user.name
    return jsonify(ret_dict)
```

#### 2.1.2 first() 

查询第一个，返回对象

```python
@app.route('/first')
def first():
    user = User.query.first() # 查询返回第一个
    return jsonify({user.mobile:user.name})
```

#### 2.1.3 get() 

根据主键ID获取对象，若主键不存在返回None

```python
@app.route('/get')
def get():
    # 根据主键ID获取对象，若主键不存在返回None
    user = User.query.get(2)
    return jsonify({user.mobile:user.name})
```

#### 2.1.4 另一种查询方式db.session.query()

```python
db.session.query(User).all()
db.session.query(User).first()
db.session.query(User).get(2)
```



### 2.2 过滤查询

#### 2.2.1 filter_by

进行过虑

```python
@app.route('/filter_by')
def filter_by():
    User.query.filter_by(mobile='18516952650').first()
    ret = User.query.filter_by(mobile='18516952650', id=1).first()  # and关系
    return ret.name
```

#### 2.2.2 filter

进行过虑

```python
@app.route('/filter')
def filter_by():
    # User.query.filter_by(mobile='18516952650').first()
    ret = User.query.filter(User.mobile=='18516952650').first()
    return ret.name
```



### 2.3 逻辑查询

#### 2.3.1 or_逻辑或

```python
from sqlalchemy import or_
@app.route('/or')
def o_r():
    # endswith(x) 表示以x结尾
    rets = User.query.filter(or_(User.mobile=='13911111111', User.name.endswith('号'))).all()
    ret_dict = {ret.mobile:ret.name for ret in rets}
    return jsonify(ret_dict)
```

#### 2.3.2 and_逻辑与

```python
from sqlalchemy import and_
@app.route('/and')
def an_d():
    # filter(and_(User.name != '13911111111', ...startswith('185'))) 表示name不是xxxx 并且mobile以185开头
    rets = User.query.filter(and_(User.name != '13911111111', User.mobile.startswith('185'))).all()
    ret_dict = {ret.mobile:ret.name for ret in rets}
    return jsonify(ret_dict)
```

#### 2.3.3 not_逻辑非

```python
from sqlalchemy import not_
@app.route('/not')
def n_ot():
    # not_(User.mobile == '13911111111') 表示mobile不是xxxx的
    rets = User.query.filter(not_(User.mobile == '13911111111')).all()
    ret_dict = {ret.mobile:ret.name for ret in rets}
    return jsonify(ret_dict)
```



### 2.4 offset偏移和limit节选

#### 2.4.1 offset

偏移，起始位置

```python
@app.route('/offset')
def offset():
    # 跳过2个，从第三个开始：offset(2)
    rets = User.query.offset(2).all()
    ret_dict = {ret.id:ret.name for ret in rets}
    return jsonify(ret_dict)
```

#### 2.4.2 limit

获取限制数据

```python
@app.route('/limit')
def limit():
    # 只选取n个：User.query.limit(n)
    rets = User.query.limit(2).all()
    ret_dict = {ret.id:ret.name for ret in rets}
    return jsonify(ret_dict)
```



### 2.5 order_by排序

排序

```python
@app.route('/order_by')
def order_by():
    # order_by(User.id.desc()) 根据ID倒序
    rets1 = User.query.order_by(User.id.desc()).all() 
    rets2 = User.query.order_by(User.id).all() # 正序
    ret_dict = {'a': str(rets1), 'b': str(rets2)}
    return jsonify(ret_dict)
```



### 2.6 高级查询

#### 2.6.1 复合查询

> 多个查询方法一起使用

```python
@app.route('/fuhe')
def fuhe():
    # 多个查询方法一起使用
    # name以13开头，倒序，跳过2个，从第三个开始，一共获取5个
    rets = User.query.filter(User.name.startswith('13')).order_by(User.id.desc()).offset(2).limit(5).all()
    ret_dict = {ret.id:ret.name for ret in rets}
    return jsonify(ret_dict)
```

```python
# User.query.filter(User.name.startswith('13')).order_by(User.id.desc()).offset(2).limit(5).all() 本质和下边代码一样
query = User.query.filter(User.name.startswith('13'))
query = query.order_by(User.id.desc())
query = query.offset(2).limit(5)
rets = query.all()
```

#### 2.6.2 load_only优化查询

> 查询指定字段
>
> - options表示选择要展示的字段，投影
> - load_only表示只读取指定字段，而不查询整条数据

```python
from sqlalchemy.orm import load_only
@app.route('/youhua')
def youhua():
    print('==') # options表示选择要展示的字段，load_only表示只读取字段，不整条数据查询
    ret = User.query.options(load_only(User.name, User.mobile)).filter_by(id=1).first()  # 查询特定字段
    User.query.filter_by(id=1).first() # 查询所有字段
    print('==')
    return '{} : {}'.format(ret.name, ret.mobile)

# select user_id, mobile,.... # 查询指定字段
# select * from   # 程序不要使用
```

#### 2.6.3 func聚合查询

> 对结果进行二次统计、运算
>
> - 需求：查询关注别人的用户id，和他关注的总人数

```python
from sqlalchemy import func # func中还有很多别的计算函数
@app.route('/juhe')
def juhe():
    # sqlalchemy.func.count(xx) 表示对xx的数量进行求和
    rets = db.session.query(Relation.user_id, func.count(Relation.target_user_id)).filter(
        Relation.relation == Relation.RELATION.FOLLOW).group_by(Relation.user_id).all()
    # 去user_relation表中查询relation是1的数据，按user_id进行分组，
    # 并返回[(user_id和，user_id相同的target_user_id数量的和),...]
    # SELECT user_relation.user_id , count(user_relation.target_user_id) 
	# FROM user_relation 
	# WHERE user_relation.relation = %s GROUP BY user_relation.user_id
    # rets = db.session.query(Relation.user_id, func.count(Relation.target_user_id))
    # print(rets)
    # rets = rets.filter(Relation.relation == Relation.RELATION.FOLLOW)
    # print(rets)
    # rets = rets.group_by(Relation.user_id).all()
    # print(rets)
    return str(rets)
```

#### 2.6.4 关联查询

> - 跨表查询，需要在一个模型类中使用relationship声明一个字段，该字段指向另外一个模型类
> - 需求：通过用户手机号码获取用户的性别

##### 1. 使用ForeignKey指定字段关联主表字段

```python
class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True, doc='用户ID')
	...
    # TODO 2. 声明一个字段，用db.relationship('UserProfile'）指向UserProfile模型类
    # 注意2.2： User.profile == UserProfile; User.profile.gender == UserProfile.gender
    # 注意2.3： User相当于UserProfile是【逻辑主表】
    # 注意2.1： uselist=False参数表示通过User.profile方式获取的只有一个数据对象
    #          uselist默认为True 表示通过User.profile方式获取是由数据对象组成的列表
    profile = db.relationship('UserProfile', uselist=False)
    
class UserProfile(db.Model):
    # TODO 1. 第三个参数db.ForeignKey('user_basic.user_id')表示外键指向user_basic表的user_id
    # 注意1.1：这里必须用原生表名和原生字段名
    # 注意1.2：这只是代码逻辑规定的关联关系，并不能对原生数据表造成任何影响
    # 注意1.3：这里是代码逻辑层面上的从表，简称【逻辑从表】，user_profile.id既是user_profile表的主键，又是【逻辑外键】
    id = db.Column('user_id', db.Integer, db.ForeignKey('user_basic.user_id'), primary_key=True, doc='用户ID')
	...
    
class Relation(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user_basic.user_id'), doc='用户ID')
    ...

# http://192.168.65.131:5000/gender?mobile=13161933310
@app.route('/gender')
def gender():
    mobile = request.args.get('mobile', None)
    if not mobile:
        return '给个手机号，我再告诉你是男是女'
    # 根据user_basic.moblie手机号查询user_profile.gender
    users = User.query.filter(User.mobile==mobile).all()
    print(users)
    user = users[0]
    return '{}, {}, {}'.format(user.name, user.mobile, str(user.profile.gender))
```

##### 2. 使用primaryjoin指明主从两表的关联字段

> 只需要在一个模型类中声明指向另外一个模型类的字段就好了，无需再使用ForeignKey


```python
class User(db.Model):
	...
    # TODO 1. 声明一个字段，用db.relationship('UserProfile'）指向UserProfile模型类，参数是类名
    # 注意1.2： User.profile == UserProfile; User.profile.gender == UserProfile.gender
    # 注意1.1： uselist=False参数表示通过User.profile方式获取的只有一个数据对象
    #          默认为True 表示通过User.profile方式获取是由数据对象组成的列表
    # TODO 2. primaryjoin='User.id==foreign(UserProfile.id)', 表示两表字段的逻辑关联
    # 注意 2： 参数primaryjoin接收是类名和类字段名
    profile = db.relationship('UserProfile',
                              primaryjoin='User.id==foreign(UserProfile.id)',
                              uselist=False)
 
class UserProfile(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True, doc='用户ID')
......
```

##### 3. 指定字段关联查询

> 以上两种方式，都是通过一个表的模型类查询另外一个表中的字段的值，那如何进行两表关联查询呢？

```python
class User(db.Model):
	...
    # TODO 1. 声明一个字段，用db.relationship('UserProfile'）指向UserProfile模型类，参数是类名
    # 注意1.2： User.profile == UserProfile; User.profile.gender == UserProfile.gender
    # 注意1.1： uselist=False参数表示通过User.profile方式获取的只有一个数据对象
    #          默认为True 表示通过User.profile方式获取是由数据对象组成的列表
    # TODO 2. primaryjoin='User.id==foreign(UserProfile.id)', 表示两表字段的逻辑关联
    # 注意 2： 参数primaryjoin接收是类名和类字段名
    profile = db.relationship('UserProfile',
                              primaryjoin='User.id==foreign(UserProfile.id)',
                              uselist=False)
 
class UserProfile(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True, doc='用户ID')
......

# http://192.168.65.131:5000/gender?mobile=13161933310
from sqlalchemy.orm import load_only, contains_eager
@app.route('/gender')
def gender():
    mobile = request.args.get('mobile', None)
    if not mobile:
        return '给个手机号，我再告诉你是男是女'
    # todo 下面是翻译
    # ret = User.query.join(User.profile)
    #   --> User表和UserProfile JOIN!
    # ret = ret.options(load_only(User.mobile),
    #                   contains_eager(User.profile).load_only(UserProfile.gender))
    #   --> options最终展示结果：load_only只查询(User.mobile)，和
    #                   contains_eager（指向User.profile的）UserProfile表的gender
    # ret = filter(User.mobile==mobile).all()
    #   --> 过滤（User.mobile是传入的参数）后，返回全部结果
    # 在User中声明了User.profile==UserProfile, 所以：
    #     1. User.query.join(User.profile)
    #     2. contains_eager(User.profile).load_only(UserProfile.gender)
    # TODO contains_eager(模型类名.指向模型的字段名)是修饰load_only(被指向的模型类名.字段名)
    rets = User.query.join(User.profile).options(
        load_only(User.mobile),
        contains_eager(User.profile).load_only(UserProfile.gender)).filter(User.mobile==mobile).all()
    print(rets)
    print(rets[0].__dict__)
    print(rets[0].__dict__['profile'].__dict__)
    user = rets[0]
    return 'mobile={}, gender={}'.format(user.mobile, user.profile.gender)
```

##### 4. 注意【重要】：

- **无论是使用ForeignKey指定字段关联主表字段，还是使用primaryjoin指明主从两表的关联字段，实际两个表在原生数据库中没有外键关联关系，都只是从代码逻辑上描述两表之间业务上的关联关系！**

  

## 3 更新

```python
@app.route('/update')
def update():
    # 方式1
    user = User.query.get(1)
    user.name = 'Python'
    db.session.add(user)
    db.session.commit()
    # 方式2
    input('sss')
    User.query.filter_by(id=1).update({'name': '黑马头条号'})
    db.session.commit()

    return 'update'
```



## 4 删除

```python
@app.route('/delete')
def delete():
    # 方式1
    user = User.query.order_by(User.id.desc()).first()
    db.session.delete(user)
    db.session.commit()
    # 方式2
    # User.query.filter(User.mobile=='18512345678').delete()
    # db.session.commit()

    return 'delete'
```



## 5 事务

> 通过db.session.rollback()来回滚

```python
@app.route('/shiwu')
def shiwu():
    # 事务
    try:
        user = User(mobile='18911111111', name='itheima')
        db.session.add(user)
        db.session.flush() # 将db.session记录的sql传到数据库中执行
        profile = UserProfile(id=user.id)
        db.session.add(profile)
        db.session.commit()
    except:
        db.session.rollback() # 这是关键：报错就回滚
    return 'shiwu'
```

- `db.session.xxx`  都是写操作相关

  ```
  db.session.add(user)
  db.session.flush()
  db.session.commit()
  db.session.rollback()
  ```

- `模型类.query.xxx` 都是读操作相关



## 6 课后阅读

https://blog.csdn.net/levon2018/article/details/82683906