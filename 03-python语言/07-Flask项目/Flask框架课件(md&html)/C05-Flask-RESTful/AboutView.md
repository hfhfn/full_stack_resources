# 关于视图

[TOC]
<!-- toc -->

## 1. 为flask restful路由起名

> 通过endpoint参数为路由起名，默认名称是视图类名的小写
>
> ```python
> api.add_resource(HelloWorldResource, '/', endpoint='HelloWorld')
> ```
>
> 验证：
>
> ```python
> print(app.url_map)
> ```

## 2. flask restful使用蓝图

> ```python
> from flask import Flask, Blueprint
> from flask_restful import Api, Resource
> 
> # 视图类
> class UserProfileResource(Resource):
>     def get(self):
>         return {'msg': 'get user profile'}
> 
> app = Flask(__name__)
> # 1. 定义蓝图
> user_bp = Blueprint('user', __name__)
> # 2. 在restful API中使用蓝图
> user_api = Api(user_bp)
> # 3. 注册API路由
> user_api.add_resource(UserProfileResource, '/users/profile', endpoint='hahaha')
> # 4. app注册蓝图
> app.register_blueprint(user_bp)
> 
> if __name__ == '__main__':
>     app.run(debug=True)
> ```

## 3. flask restful视图使用装饰器

> - 使用视图类属性`method_decorators`添加装饰器
>
>   > - 接收列表：
>   >   - 视图类中所有方法都被装饰
>   >   - 可以有多个装饰器
>   > - 接收字典：
>   >   - 视图类中规定的方法被装饰
>   >   - 可以有多个装饰器
>
> ```python
> from flask import Flask, Blueprint
> from flask_restful import Api, Resource
> 
> 
> def decorator1(func):
>     def wrapper(*args, **kwargs):
>         print('decorator1')
>         return func(*args, **kwargs)
>     return wrapper
> 
> def decorator2(func):
>     def wrapper(*args, **kwargs):
>         print('decorator2')
>         return func(*args, **kwargs)
>     return wrapper
> 
> # 视图类
> class UserProfileResource(Resource):
>     # 为类视图中的所有方法添加装饰器
>     # method_decorators = [decorator1, decorator2]
>     # 为类视图中不同的方法添加不同的装饰器
>     method_decorators = {'get': [decorator1, decorator2],
>                          'post': [decorator1]}
>     def get(self):
>         return {'msg': 'get'}
>     def post(self):
>         return {'msg': 'post'}
> 
> app = Flask(__name__)
> # 1. 定义蓝图
> user_bp = Blueprint('user', __name__)
> # 2. 在restful API中使用蓝图
> user_api = Api(user_bp)
> # 3. 注册API路由
> user_api.add_resource(UserProfileResource, '/users/profile', endpoint='hahaha')
> # 4. app注册蓝图
> app.register_blueprint(user_bp)
> 
> if __name__ == '__main__':
>     app.run(debug=True)
> ```
>
> - 测试代码
>
> ```python
> import requests
> 
> url = 'http://127.0.0.1:5000/users/profile'
> 
> resp = requests.get(url)
> print(resp.json())
> 
> resp = requests.post(url)
> print(resp.text)
> ```

  

