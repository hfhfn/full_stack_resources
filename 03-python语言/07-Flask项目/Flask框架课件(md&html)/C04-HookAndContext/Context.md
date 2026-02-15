# 上下文

> 上下文：即语境，语意，在程序中可以理解为在代码执行到某一时刻时，根据之前代码所做的操作以及下文即将要执行的逻辑，可以决定在当前时刻下可以使用到的变量，或者可以完成的事情。
>
> - Flask中有两种上下文，请求上下文和应用上下文：
>   - 请求上下文	
>     - request 
>     - session
>     - request_context
>   - 应用上下文 
>     - current_app 
>     - g对象
>     - app_context
> - Flask中上下文对象：相当于一个容器，保存了 Flask 程序运行过程中的一些信息。

[TOC]
<!-- toc -->

## 1. 请求上下文(request context)

> 思考：在视图函数中，如何取到当前请求的相关数据？比如：请求地址，请求方式，cookie等等
>
> 在 flask 中，可以直接在视图函数中使用 **request** 这个对象进行获取相关数据，而 **request** 就是请求上下文的请求对象，保存了当前本次请求的相关数据；另外还有**session**
>
> - request 
>
>   - 封装了HTTP请求的内容，针对的是http请求。举例：user = request.args.get('user')，获取的是get请求的参数。
>   - 每一次请求周期结束后，都会清空该次请求的相关信息
>
> - session
>
>   - 用来记录请求会话中的信息，针对的是用户信息。举例：session['name'] = user.id，可以记录用户信息。还可以通过session.get('name')获取用户信息。
>   - 每一次请求周期结束后，都会清空该次请求的相关信息
>
> - request_context【拓展】
>
>   > `request_context`为我们提供了请求上下文环境，允许我们在外部使用请求上下文`request`、`session`
>   >
>   > 可以通过with语句进行使用
>   >
>   > ```python
>   > # 注意：在python终端/python console中进行下面的代码
>   > from flask import Flask, request
>   > app = Flask('')
>   > request.args  
>   > # 此时输出一坨异常信息，因为没有上下文环境
>   > environ = {'wsgi.version':(1,0), 'wsgi.input': '', 'REQUEST_METHOD': 'GET', 'PATH_INFO': '/hahahhaha', 'SERVER_NAME': 'itcast server', 'wsgi.url_scheme': 'http', 'SERVER_PORT': '80'}
>   > # environ模拟了解析客户端请求之后的wsgi字典数据
>   > with app.request_context(environ):  # 借助with语句使用request_context创建请求上下文
>   > 	print(request.path)  
>   > # 成功输出：/hahahhaha
>   > ```

## 2. 应用上下文(application context)

> 它的字面意思是 应用上下文，但它不是一直存在的，它只是request context 中的一个对 app 的代理(人)，所谓local proxy。它的作用主要是帮助 request 获取当前的应用，它是伴 request 而生，随 request 而灭的。
>
> - 应用上下文对象有：
>   - current_app
>   - g
>   - app_context

### 2.1 current_app

> - 应用程序上下文,用于存储应用程序中的变量，可以通过current_app.name打印当前app的名称，也可以在current_app中存储一些变量，例如：
>
>   > - 应用的启动脚本是哪个文件，启动时指定了哪些参数
>   > - 加载了哪些配置文件，导入了哪些配置
>   > - 连了哪个数据库
>   > - 有哪些public的工具类、常量
>   > - 应用跑在哪个机器上，IP多少，内存多大
>
> - 示例
>
>   ```python
>   from flask import Flask, current_app
>   
>   app = Flask(__name__)
>   
>   # 为了方便在各个视图中使用，可以将一些自定义内容保存到flask app中
>   # 后续可以在视图中使用current_app.xxx获取
>   app.xxx = '这个app.xxx中的xxx是我自己起的名字'
>   
>   @app.route('/1')
>   def route1():
>       return current_app.xxx
>   
>   @app.route('/2')
>   def route2():
>       return current_app.xxx
>   
>   if __name__ == '__main__':
>       app.run(debug=True)
>   ```
>
> - 结论：
>
>   - **`current_app` 就是当前运行的flask app，在代码不方便直接操作flask的app对象时，可以操作`current_app`就等价于操作flask app对象**

### 2.2 g对象

> g 作为 flask 程序全局的一个临时变量，充当中间媒介的作用，我们可以通过它在一次请求调用的多个函数间传递一些数据。每次请求都会重设这个变量。
>
> ```python
> from flask import Flask, request, g
> 
> app = Flask(__name__)
> 
> def db_query():
>     print('user_id={} user_name={}'.format(g.user_id, g.user_name))
> 
> @app.route('/')
> def index():
>     g.user_id = request.args['user_id']
>     g.user_name = request.args['name']
>     db_query()
>     return 'user_id={} user_name={}'.format(g.user_id, g.user_name)
> 
> if __name__ == '__main__':
>     app.run(debug=True)
>     # http://127.0.0.1:5000/?user_id=1&name=白色哈士奇
>     # http://127.0.0.1:5000/?user_id=2&name=黑色哈士奇
> ```
>
> - 重要结论：**g对象和request对象一样：生命周期只在那一次完整的请求中**

### 2.3 拓展:`app_context`

> `app_context`为我们提供了应用上下文环境，允许我们在外部使用应用上下文`current_app`、`g`等
>
> 和`request_context`一样，可以通过`with`语句进行使用
>
> ```python
> # 注意：在python终端/python console中进行下面的代码
> from flask import Flask, current_app
> app = Flask('')
> app.zuozhe = '无敌哈士奇'
> current_app.zuozhe
> # 一大坨报错信息，原因：没有上下文环境
> # 借助with语句使用app_context创建应用上下文
> with app.app_context():  
> 	print(current_app.zuozhe)
> # 成功输出：'无敌哈士奇'
> ```

## 3. 案例

> 模拟用户访问个人中心涉及的权证认证场景

#### 3.1 需求:写一个flask项目符合下列要求

> - 技术要求使用`session`、`g对象`、`请求钩子`
> - 接口要求
>   - `/`
>     - 如果未登录，返回`首页`
>     - 如果已登录，返回`欢迎回来，xxx`
>   - `/user`
>     - 如果未登录，返回`无法访问个人中心，请登录`
>     - 如果已登录，返回`个人中心`
>   - `/login`
>     - 模拟登录，用户查询字符串传递用户昵称


#### 3.2 代码实现

> ```python
> from flask import Flask, session, g, abort
> 
> app = Flask(__name__)
> app.secret_key = 'fdsfsdf'
> 
> @app.errorhandler(401)
> def error_handler(e):
>     return '无法访问个人中心，请登录'
> 
> # 使用请求钩子，把用户信息保存在g变量中
> @app.before_request
> def get_user_info():
>     """获取用户信息，其实就是获取认证信息"""
>     g.name = session.get('name', None)
> 
> # 需求：对指定的/user视图进行访问限制 如个人中心必须登录后才能访问
> # 解决办法：   方案1：把需要限制访问的视图放入蓝图中，对蓝图设置请求钩子
> # 这里采用：   方案2：实现装饰器
> def login_required(func):
>     def wrapper(*args, **kwargs):
>         if g.name: # 已登录，允许执行视图函数
>             return func(*args, **kwargs)
>         else:
>             # 400 语法/参数错误 401 未认证 403 已认证但权限不够
>             # 404 资源不存在 405 请求方式不支持
>             abort(401)
>     return wrapper
> 
> @app.route('/user')
> @login_required
> def user(): # 需要已登录状态才能访问
>     return '个人中心'
> 
> @app.route('/')
> def index():
>     if g.name: # 已经登录
>         return '欢迎回来，%s' % g.name
>     else: # 未登录
>         return '首页'
> 
> @app.route('/login')
> def login():
>     # 模拟用户
>     session['name'] = '无敌哈士奇' # 登录成功，记录认证信息
>     return '用户登录'
> 
> if __name__ == '__main__':
>     app.run(debug=True)
> ```





