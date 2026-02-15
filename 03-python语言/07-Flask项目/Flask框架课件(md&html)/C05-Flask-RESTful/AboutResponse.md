# 关于响应处理

[TOC]
<!-- toc -->

## 1. 序列化数据

> Flask-RESTful 提供了marshal工具，用来帮助我们将数据序列化为特定格式的字典数据，以便作为视图的返回值。

### 1.1 步骤

> - step 1. 定义要返回数据格式，dict
>
> - step 2. 在具体的视图函数中返回序列化的数据
>
>   - 对视图函数使用`marshal_with`装饰器
>   
>     - `@marshal_with(step1定义的数据格式, envelope='返回数据的外层包裹字段')`
>     - 在视图函数中使用`marshal`函数
>       - `marshal(实例化的数据类, step1定义的数据格式, envelope='返回数据的外层包裹字段')`

### 1.2 代码实现

> ```python
> from flask import Flask
> from flask_restful import fields, marshal, marshal_with, Resource, Api
> 
> # 用来模拟要返回的数据对象的类
> class User(object):
>     def __init__(self, user_id, name, age):
>         self.user_id = user_id
>         self.name = name
>         self.age = age
> 
> # TODO 定义要返回数据格式
> resoure_fields = {
>         'user_id': fields.Integer,
>         'name': fields.String
>     }
> 
> class Demo1Resource(Resource):
>     # TODO 使用装饰器marshal_with让视图函数返回序列化的数据
>     # envelope参数规定了返回数据的外层包裹字段
>     @marshal_with(resoure_fields, envelope='data1')
>     def get(self):
>         # 直接返回实例化的具体的数据对象
>         return User(1, 'itcast', 12)
> 
> class Demo2Resource(Resource):
>     def get(self):
>         user = User(1, 'itcast', 12)
>         # TODO 使用marshal函数返回序列化的数据
>         return marshal(user, resoure_fields, envelope='data2')
> 
> app = Flask(__name__)
> # 创建api对象，加载app对象
> api = Api(app)
> # 添加类视图
> api.add_resource(Demo1Resource, '/1')
> api.add_resource(Demo2Resource, '/2')
> 
> if __name__ == '__main__':
>     app.run(debug=True)
> ```

## 2. 定制返回的JSON格式

### 2.1 需求

> - 想要接口返回的JSON数据具有如下统一的格式
>
>  ```python
> {"message": "描述信息", "data": {要返回的具体数据}}
>     ```
>    
>      - 在接口处理正常的情况下， message返回ok即可，但每个接口只返回要返回的具体数据
>
>  ```python
> class DemoResource(Resource):
>         def get(self):
>             return {'user_id':1, 'name': 'itcast'}
>     ```
>    
>    - marshal函数或marshal_with装饰器，都只能通过envelope参数控制外层字段，那上述需求如何满足呢？

### 2.2 解决

> - Flask-RESTful的Api对象提供了一个`representation`的装饰器，允许定制返回数据的呈现格式，该装饰器使用方法如下：
>
>   > ```python
>   > # 伪代码
>   > api = flask_restful.Api(flask.Flask(__name__))
>   > @api.representation('application/json')
>   > def handle_json(data, code, headers):
>   >    # TODO 此处添加自定义处理
>   >    return resp
>   > ```
>
> - 从`flask_restful.representations.json`中复制`output_json`函数，改写并添加`representation`装饰器

### 2.3 完整代码如下

>```python
>from six import PY3
>from json import dumps
>from flask import Flask, make_response, current_app
>from flask_restful import fields, marshal, marshal_with, Resource, Api
>
># 用来模拟要返回的数据对象的类
>class User(object):
>    def __init__(self, user_id, name, age):
>        self.user_id = user_id
>        self.name = name
>        self.age = age
>
># TODO 定义要返回数据格式
>resoure_fields = {
>        'user_id': fields.Integer,
>        'name': fields.String
>    }
>
>class Demo1Resource(Resource):
>    # TODO 使用装饰器marshal_with让视图函数返回序列化的数据
>    # envelope参数规定了返回数据的外层包裹字段
>    @marshal_with(resoure_fields)
>    def get(self):
>        # 直接返回实例化的具体的数据对象
>        return User(1, 'itcast', 12)
>
>class Demo2Resource(Resource):
>    def get(self):
>        user = User(1, 'itcast', 12)
>        # TODO 使用marshal函数返回序列化的数据
>        return marshal(user, resoure_fields)
>
>app = Flask(__name__)
># 创建api对象，加载app对象
>api = Api(app)
># 添加类视图
>api.add_resource(Demo1Resource, '/1')
>api.add_resource(Demo2Resource, '/2')
>
># TODO 1. 自定义返回数据的格式: 重写output_json函数，该函数位置：flask_restful.representations.json
># TODO 2. Flask-RESTful的Api对象提供了一个representation装饰器，允许定制返回数据的呈现格式
># TODO 3. 传入参数声明：只要是返回的是'application/json'类型的数据，就执行重写的output_json函数
># from flask_restful.representations.json import output_json
>@api.representation('application/json')
>def output_json(data, code, headers=None):
>    """Makes a Flask response with a JSON encoded body"""
>
>    # 此处为自己添加***************
>    if 'message' not in data:
>        data = {
>            'message': 'OK',
>            'data': data
>        }
>    # **************************
>
>    settings = current_app.config.get('RESTFUL_JSON', {})
>
>    # If we're in debug mode, and the indent is not set, we set it to a
>    # reasonable value here.  Note that this won't override any existing value
>    # that was set.  We also set the "sort_keys" value.
>    if current_app.debug:
>        settings.setdefault('indent', 4)
>        settings.setdefault('sort_keys', not PY3)
>
>    # always end the json dumps with a new line
>    # see https://github.com/mitsuhiko/flask/pull/1262
>    dumped = dumps(data, **settings) + "\n"
>
>    resp = make_response(dumped, code)
>    resp.headers.extend(headers or {})
>    return resp
>
>if __name__ == '__main__':
>    app.run(debug=True)
>```
>







