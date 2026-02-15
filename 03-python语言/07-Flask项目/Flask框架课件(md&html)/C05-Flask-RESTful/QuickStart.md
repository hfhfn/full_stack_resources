# flask-restful的helloworld

> **Flask-RESTful是用于快速构建REST API的Flask扩展模块。**

[TOC]
<!-- toc -->

## 1. 安装

> ```shell
> pip install flask-restful
> ```

## 2. Hello World

> ```python
> from flask import Flask
> from flask_restful import Resource, Api
> 
> app = Flask(__name__)
> # 1. 创建api对象，加载app对象
> api = Api(app)
> 
> # 2. 定义视图类 继承Resource
> class HelloWorldResource(Resource):
>     # 类视图的响应content-type会自动设为application/json
>     # 类视图方法直接返回字典，能自动序列化为json返回给客户端
>     # 类视图的方法名对应请求方式
>     def get(self):
>         return {'hello': 'world'}
> 
>     def post(self):
>         return {'msg': 'post hello world'}
> 
> # 3. 添加类视图
> api.add_resource(HelloWorldResource, '/')
> 
> if __name__ == '__main__':
>     app.run(debug=True)
> ```
>
> - 测试代码：
>
> ```python
> import requests
> 
> url = 'http://127.0.0.1:5000/'
> 
> resp = requests.get(url)
> print(resp.json())
> 
> resp = requests.post(url)
> print(resp.text)
> ```