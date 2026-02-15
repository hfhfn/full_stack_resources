# 路由

> ```python
> @app.route("/itcast")
> def view_func():
>     return "hello world"
> ```

[TOC]
<!-- toc -->

## 1. 查询路由信息 

### 1.1 命令行方式

> ```shell
> export FLASK_APP=helloworld
> flask routes
> # 输出类似下面的信息
> Endpoint  Methods  Rule
> --------  -------  -----------------------
> index     GET      /
> static    GET      /static/<path:filename>
> ```

### 1.2 在程序中获取

> - 在应用（实例化的flask app）中的url_map属性中保存着整个Flask应用的路由映射信息，可以通过读取这个属性获取路由信息
>
> ```python
> print(app.url_map)
> ```
>
> - 如果想在程序中遍历路由信息，可以采用如下方式
>
> ```python
> for rule in app.url_map.iter_rules():
>     print('name={} path={}'.format(rule.endpoint, rule.rule))
> ```

### 1.3 练习

> - 需求
>
>   - 通过访问`/`地址，以json的方式返回应用内的所有路由信息
>
> - 实现
>
>   > ```python
>   > import json
>   > from flask import Flask
>   > app = Flask(__name__)
>   > 
>   > @app.route('/')
>   > def route_map():
>   >  """返回所有视图网址"""
>   >  rules_iterator = app.url_map.iter_rules()
>   >  return json.dumps({rule.endpoint: rule.rule for rule in rules_iterator})
>   > 
>   > if __name__ == '__main__':
>   >  app.run()
>   > ```

## 2. 指定请求方式

> - 在 Flask 中，如果不显式声明请求方式，其默认的请求方式有：
>   - GET
>   - OPTIONS(自带)
>   - HEAD(自带)
>
> - 利用`methods`参数可以自己指定一个接口的请求方式
>
> ```python
> from flask import Flask, request
> app = Flask(__name__)
> 
> @app.route("/itcast1", methods=["POST"])
> def view_func_1():
>    return "hello world 1"
> # methods参数接收一个list，请求方式为大写字符，可以有多个请求方式
> @app.route("/itcast2", methods=["GET", "POST"])
> def view_func_2():
>    # 利用flask.request.method判断是哪种请求方式
>    if request.method == 'GET': 
>        return "hello world 2, get"
>    if request.method == 'POST':
>        return "hello world 2, post"
> 
> if __name__ == '__main__':
>    app.run()
> ```
>
> - 利用requests模块测试上述代码
>
>   > `pip install requests`安装`requests`模块
>   >
>   > ```python
>   > import requests                                     
>   >                                                    
>   > url1 = 'http://127.0.0.1:5000/itcast1'              
>   > resp = requests.head(url1)                          
>   > print(resp.__dict__)                                
>   > resp = requests.options(url1)                       
>   > print(resp.__dict__)                                
>   > resp = requests.post(url1)                          
>   > print(resp.text)                                    
>   >                                                    
>   > url2 = 'http://127.0.0.1:5000/itcast2'              
>   > resp = requests.post(url2)                          
>   > print(resp.text)                                    
>   > resp = requests.get(url2)                           
>   > print(resp.text)                                    
>   > ```
>
