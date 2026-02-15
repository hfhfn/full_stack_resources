# SQLAlchemy映射构建

[TOC]

<!-- toc -->

## 1 简介

> **SQLAlchemy**是Python编程语言下的一款开源软件。提供了SQL工具包及对象关系映射（ORM）工具，使用MIT许可证发行。
>
> SQLAlchemy“采用简单的Python语言，为高效和高性能的数据库访问设计，实现了完整的企业级持久模型”。
>
> SQLAlchemy首次发行于2006年2月，并迅速地在Python社区中最广泛使用的ORM工具之一，不亚于Django的ORM框架。
>
> **Flask-SQLAlchemy**是在Flask框架的一个扩展，其对**SQLAlchemy**进行了封装，目的于简化在 Flask 中 SQLAlchemy 的 使用，提供了有用的默认值和额外的助手来更简单地完成日常任务。

## 2 安装

> 安装Flask-SQLAlchemy

```shell
pip install flask-sqlalchemy
```

> 注意：如果使用的是MySQL数据库，还需要安装MySQL的Python客户端库

```shell
pip install mysqlclient
```

> 如果`pip install mysqlclient`抛出`OSError: mysql_config not found`异常，还需要安装`libmysqlclient-dev`

```shell
sudo apt-get install libmysqlclient-dev
```

## 3 在flask中配置数据库连接设置并写入数据

> 在Flask中使用Flask-SQLAlchemy需要进行配置，主要配置以下几项：
>
> - `SQLALCHEMY_DATABASE_URI` 数据库的连接信息
>
>   > - Postgres:
>   >
>   > ```
>   > postgresql://user:password@localhost/mydatabase
>   > ```
>   >
>   > - MySQL:
>   >
>   > ```
>   > mysql://user:password@localhost/mydatabase
>   > ```
>   >
>   > - Oracle:
>   >
>   > ```
>   > oracle://user:password@127.0.0.1:1521/sidname
>   > ```
>   >
>   > - SQLite （注意开头的四个斜线）:
>   >
>   > ```
>   > sqlite:////absolute/path/to/foo.db
>   > ```
>   >
>   > - 不支持MongDB
>
> - `SQLALCHEMY_TRACK_MODIFICATIONS` 在Flask中是否追踪数据修改
>
> - `SQLALCHEMY_ECHO` 显示生成的SQL语句，可用于调试
>
> 上述这些配置参数需要放在Flask的应用配置（`app.config`）中

### 3.1 flask中代码实现

> - **配置连接并构建模型类映射关系**
>
>   > - 首先我们按照1.2章节-项目介绍-Pycharm远程开发中的步骤设置好开发环境，并在项目路径下创建`Test/2_sqlalchemy/2_1_sqlalchemy.py`文件
>   >
>   > - 在远程服务器上的mysql中创建名为`test43`的数据库
>   >
>   >   - 字符集：`utf8mb4` 或`utf8`
>   >
>   >     > MySQL在5.5.3之后增加了这个utf8mb4的编码，mb4就是most bytes 4的意思，专门用来兼容四字节的unicode。好在utf8mb4是utf8的超集，除了将编码改为utf8mb4外不需要做其他转换。当然，为了节省空间，一般情况下使用utf8也就够了。
>   >
>   >   - [数据库排序规则](https://www.cnblogs.com/sxdcgaq8080/p/9932807.html)：`utfmb4_general_ci`或`utf_general_ci`
>   >
>   > - 最后在`2_1_sqlalchemy.py`中完成并运行下边的代码
>   >
>   >   ```python
>   >   from flask import Flask
>   >   from flask_sqlalchemy import SQLAlchemy
>   >   
>   >   app = Flask(__name__)
>   >   # step 1. 配置sqlalchemy
>   >   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/test43' # 数据库连接地址
>   >   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 是否追踪数据库修改, 开启后影响性能
>   >   app.config['SQLALCHEMY_ECHO'] = True  # 开启后, 可以在控制台打印底层执行的sql语句
>   >   
>   >   # step 2. 创建数据库连接对象
>   >   db = SQLAlchemy(app)
>   >   
>   >   # step 3. 建立映射模型  类->表  类属性->字段  对象->记录
>   >   # 此时数据库里一个表都没有
>   >   class User(db.Model):
>   >      __tablename__ = 't_user'  # 设置表名 
>   >      id = db.Column(db.Integer, primary_key=True)  # 主键  默认主键自增
>   >      name = db.Column(db.String(20), unique=True)  # 设置唯一
>   >      age = db.Column(db.Integer, doc='年龄int') # doc字段说明，和数据表没有关联性
>   >      gender = db.Column(db.SmallInteger, default=0, doc='性别，默认0')
>   >   
>   >   @app.route('/')
>   >   def index():
>   >       return "index"
>   >   
>   >   if __name__ == '__main__':
>   >       db.drop_all()  # 删除所有继承自db.Model的表
>   >       db.create_all()  # 创建所有继承自db.Model的表 # 在这里建立了表格
>   >       app.run(debug=False)
>   >   ```
>
> - **写入数据**
>
>   > 修改代码如下，并再次运行
>
>   ```python
>   # 建立映射模型  类->表  类属性->字段  对象->记录
>   # 此时数据库中已经存在了t_user表
>   # class User(db.Model):
>   class t_user(db.Model): # 也可以用模型类的类名指向数据库的表名
>      # __tablename__ = 't_user'  # 设置表名  
>      id = db.Column(db.Integer, primary_key=True)  # 主键  默认主键自增
>      name = db.Column(db.String(20), unique=True)  # 设置唯一
>      age = db.Column(db.Integer)
>      # 把性别字段注释掉再写入数据发现：sqlalchemy的模型类和数据表无需一一对应，但还是建议把所有字段都写出来
>      # gender = db.Column(db.SmallInteger, default=0) # 性别，SmallInteger，默认为0
>   
>   @app.route('/')
>   def add_data():
>       """增加数据"""
>       # 1.创建数据对象
>       user1 = t_user(name='gfgf', age=85)
>       # user1.age = 80 # 也可以创建数据对象后，修改数据
>   
>       # 2.添加到会话中 (转为成对应的sql语句)
>       db.session.add(user1)
>       # 添加多个数据
>       # db.session.add_all([user1, user2, user3])
>   
>       # sqlalchemy会自动创建隐式的事务, 并将sql操作添加到事务中
>       # 3.提交会话, 此时就会提交事务, 事务提交失败, 会自动回滚
>       db.session.commit()
>   
>       return "add_data"
>   ```



### 3.2 其他配置参考如下[查表]

| 名字                        | 备注                                                         |
| :-------------------------- | :----------------------------------------------------------- |
| SQLALCHEMY\_DATABASE\_URI   | 用于连接的数据库 URI 。例如:sqlite:////tmp/test.dbmysql://username:password@server/db |
| SQLALCHEMY\_BINDS           | 一个映射 binds 到连接 URI 的字典。更多 binds 的信息见[_用 Binds 操作多个数据库_](http://docs.jinkan.org/docs/flask-sqlalchemy/binds.html#binds)。 |
| SQLALCHEMY\_ECHO            | 如果设置为Ture， SQLAlchemy 会记录所有 发给 stderr 的语句，这对调试有用。\(打印sql语句\) |
| SQLALCHEMY\_RECORD\_QUERIES | 可以用于显式地禁用或启用查询记录。查询记录 在调试或测试模式自动启用。更多信息见get\_debug\_queries\(\)。 |
| SQLALCHEMY\_NATIVE\_UNICODE | 可以用于显式禁用原生 unicode 支持。当使用 不合适的指定无编码的数据库默认值时，这对于 一些数据库适配器是必须的（比如 Ubuntu 上 某些版本的 PostgreSQL ）。 |
| SQLALCHEMY\_POOL\_SIZE      | 数据库连接池的大小。默认是引擎默认值（通常 是 5 ）           |
| SQLALCHEMY\_POOL\_TIMEOUT   | 设定连接池的连接超时时间。默认是 10 。                       |
| SQLALCHEMY\_POOL\_RECYCLE   | 多少秒后自动回收连接。这对 MySQL 是必要的， 它默认移除闲置多于 8 小时的连接。注意如果 使用了 MySQL ， Flask-SQLALchemy 自动设定 这个值为 2 小时。 |



## 4. [查表]模型类字段与选项


#### 4.1 字段类型

| 类型名 | python中类型 | 说明 |
| :--- | :--- | :--- |
| Integer | int | 普通整数，一般是32位 |
| SmallInteger | int | 取值范围小的整数，一般是16位 |
| BigInteger | int或long | 不限制精度的整数 |
| Float | float | 浮点数 |
| Numeric | decimal.Decimal | 普通整数，一般是32位 |
| String | str | 变长字符串 |
| Text | str | 变长字符串，对较长或不限长度的字符串做了优化 |
| Unicode | unicode | 变长Unicode字符串 |
| UnicodeText | unicode | 变长Unicode字符串，对较长或不限长度的字符串做了优化 |
| Boolean | bool | 布尔值 |
| Date | datetime.date | 时间 |
| Time | datetime.datetime | 日期和时间 |
| LargeBinary | str | 二进制文件 |

#### 4.2 列选项

| 选项名 | 说明 |
| :--- | :--- |
| primary\_key | 如果为True，代表表的主键 |
| unique | 如果为True，代表这列不允许出现重复的值 |
| index | 如果为True，为这列创建索引，提高查询效率 |
| nullable | 如果为True，允许有空值，如果为False，不允许有空值 |
| default | 为这列定义默认值 |

#### 4.3 关系选项

| 选项名 | 说明 |
| :--- | :--- |
| backref | 在关系的另一模型中添加反向引用 |
| primary join | 明确指定两个模型之间使用的联结条件 |
| uselist | 如果为False，不使用列表，而使用标量值 |
| order\_by | 指定关系中记录的排序方式 |
| secondary | 指定多对多关系中关系表的名字 |
| secondary join | 在SQLAlchemy中无法自行决定时，指定多对多关系中的二级联结条件 |



## 5. 动手练 构建模型类映射

> 例用虚拟机中已有的头条数据库，构建模型类映射，以下面三张表为例

```sql
CREATE TABLE `user_basic` (
  `user_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `account` varchar(20) COMMENT '账号',
  `email` varchar(20) COMMENT '邮箱',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态，是否可用，0-不可用，1-可用',
  `mobile` char(11) NOT NULL COMMENT '手机号',
  `password` varchar(93) NULL COMMENT '密码',
  `user_name` varchar(32) NOT NULL COMMENT '昵称',
  `profile_photo` varchar(128) NULL COMMENT '头像',
  `last_login` datetime NULL COMMENT '最后登录时间',
  `is_media` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否是自媒体，0-不是，1-是',
  `is_verified` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否实名认证，0-不是，1-是',
  `introduction` varchar(50) NULL COMMENT '简介',
  `certificate` varchar(30) NULL COMMENT '认证',
  `article_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '发文章数',
  `following_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '关注的人数',
  `fans_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '被关注的人数',
  `like_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '累计点赞人数',
  `read_count` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '累计阅读人数',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `mobile` (`mobile`),
  UNIQUE KEY `user_name` (`user_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户基本信息表';

CREATE TABLE `user_profile` (
  `user_id` bigint(20) unsigned NOT NULL COMMENT '用户ID',
  `gender` tinyint(1) NOT NULL DEFAULT '0' COMMENT '性别，0-男，1-女',
  `birthday` date NULL COMMENT '生日',
  `real_name` varchar(32) NULL COMMENT '真实姓名',
  `id_number` varchar(20) NULL COMMENT '身份证号',
  `id_card_front` varchar(128) NULL COMMENT '身份证正面',
  `id_card_back` varchar(128) NULL COMMENT '身份证背面',
  `id_card_handheld` varchar(128) NULL COMMENT '手持身份证',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `register_media_time` datetime NULL COMMENT '注册自媒体时间',
  `area` varchar(20) COMMENT '地区',
  `company` varchar(20) COMMENT '公司',
  `career` varchar(20) COMMENT '职业',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户资料表';

CREATE TABLE `user_relation` (
  `relation_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `user_id` bigint(20) unsigned NOT NULL COMMENT '用户ID',
  `target_user_id` bigint(20) unsigned NOT NULL COMMENT '目标用户ID',
  `relation` tinyint(1) NOT NULL DEFAULT '0' COMMENT '关系，0-取消，1-关注，2-拉黑',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`relation_id`),
  UNIQUE KEY `user_target` (`user_id`, `target_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户关系表';
```



### 定义模型类的参考代码

```python
class User(db.Model):
    """
    用户基本信息
    """
    __tablename__ = 'user_basic'

    class STATUS:
        ENABLE = 1
        DISABLE = 0

    id = db.Column('user_id', db.Integer, primary_key=True, doc='用户ID')
    mobile = db.Column(db.String, doc='手机号')
    password = db.Column(db.String, doc='密码')
    name = db.Column('user_name', db.String, doc='昵称')
    profile_photo = db.Column(db.String, doc='头像')
    last_login = db.Column(db.DateTime, doc='最后登录时间')
    is_media = db.Column(db.Boolean, default=False, doc='是否是自媒体')
    is_verified = db.Column(db.Boolean, default=False, doc='是否实名认证')
    introduction = db.Column(db.String, doc='简介')
    certificate = db.Column(db.String, doc='认证')
    article_count = db.Column(db.Integer, default=0, doc='发帖数')
    following_count = db.Column(db.Integer, default=0, doc='关注的人数')
    fans_count = db.Column(db.Integer, default=0, doc='被关注的人数（粉丝数）')
    like_count = db.Column(db.Integer, default=0, doc='累计点赞人数')
    read_count = db.Column(db.Integer, default=0, doc='累计阅读人数')

    account = db.Column(db.String, doc='账号')
    email = db.Column(db.String, doc='邮箱')
    status = db.Column(db.Integer, default=1, doc='状态，是否可用')

class UserProfile(db.Model):
    """
    用户资料表
    """
    __tablename__ = 'user_profile'

    class GENDER:
        MALE = 0
        FEMALE = 1

    id = db.Column('user_id', db.Integer, primary_key=True, doc='用户ID')
    gender = db.Column(db.Integer, default=0, doc='性别')
    birthday = db.Column(db.Date, doc='生日')
    real_name = db.Column(db.String, doc='真实姓名')
    id_number = db.Column(db.String, doc='身份证号')
    id_card_front = db.Column(db.String, doc='身份证正面')
    id_card_back = db.Column(db.String, doc='身份证背面')
    id_card_handheld = db.Column(db.String, doc='手持身份证')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')
    register_media_time = db.Column(db.DateTime, doc='注册自媒体时间')

    area = db.Column(db.String, doc='地区')
    company = db.Column(db.String, doc='公司')
    career = db.Column(db.String, doc='职业')


class Relation(db.Model):
    """
    用户关系表
    """
    __tablename__ = 'user_relation'

    class RELATION:
        DELETE = 0
        FOLLOW = 1
        BLACKLIST = 2

    id = db.Column('relation_id', db.Integer, primary_key=True, doc='主键ID')
    user_id = db.Column(db.Integer, doc='用户ID')
    target_user_id = db.Column(db.Integer, doc='目标用户ID')
    relation = db.Column(db.Integer, doc='关系')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')

```



## 6. 总结

> - 配置连接并构建模型类映射关系
>
>   ```python
>   # step 1. 配置sqlalchemy
>   class Config(object):
>       SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/test43' # 数据库连接地址
>       SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据库修改, 开启后影响性能
>       SQLALCHEMY_ECHO = True # 开启后, 可以在控制台打印底层执行的sql语句
>   app.config.from_object(Config)
>   # step 2. 创建数据库连接对象
>   db = SQLAlchemy(app)
>   # step 3. 建立映射模型  类->表  类属性->字段  对象->记录
>   class User(db.Model):
>      __tablename__ = 't_user'  # 设置表名  表名默认为类名
>      id = db.Column(db.Integer, primary_key=True)  # 主键  默认主键自增
>      ...
>   ```
>
> - 模型类的构建
>
>   ```python
>   class Relation(db.Model): 
>       # 继承db.Model
>       # db = flask_sqlalchemy.SQLAlchemy(flask.Flask(__name__))
>       """
>       用户关系表
>       """
>       __tablename__ = 'user_relation' # 数据表名称
>   
>       class RELATION: # 可以类中自定义类，用于规定的字段的值
>           # 用户关系
>           DELETE = 0 # 取消关注
>           FOLLOW = 1 # 关注
>           BLACKLIST = 2 # 拉黑
>   	
>       # 'relation_id'是数据表中字段名：声明的模型类字段名和数据表字段名可以不一致
>       # primary_key=True表示该字段是主键，数据表默认该主键自增：先建库表后写模型类的好处
>       id = db.Column('relation_id', db.Integer, primary_key=True, doc='主键ID')
>       # user_id就是数据表中的字段名
>       user_id = db.Column(db.Integer, doc='用户ID')
>       # doc参数用于描述字段信息，和数据表没有关联性
>       target_user_id = db.Column(db.Integer, doc='目标用户ID')
>       # default参数规定了字段的默认值
>       relation = db.Column(db.Integer, default=RELATION.DELETE, doc='关系')
>       # db.DateTime的数据类型等同于datetime.datetime.now的格式：utc时间格式
>       ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
>       utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')
>   ```
>
> - 写入数据
>
>   ```python
>   # 1.创建数据对象，实例化模型类
>   user1 = t_user(name='gfgf', age=85)
>   # user1.age = 80 # 也可以创建数据对象后，修改数据
>   
>   # 2.添加到会话中 (转为成对应的sql语句)
>   # db.session.add_all([user1, user2, user3]) # 添加多个数据
>   db.session.add(user1)
>   
>   # 3.提交会话, 此时就会提交事务, 事务提交失败, 会自动回滚
>   db.session.commit() # sqlalchemy会自动创建隐式的事务, 并将sql操作添加到事务中发
>   ```
>
> - 先用原生SQL或其他手段创建数据库表，再编写模型类作映射
>
>   - 可以很好的控制数据库表结构的任何细节，避免发生迁移错误
>   - 后期写模型类的代码以及做增删改查非常方便，不用过分考虑表结构字段的各种细节
>
>   