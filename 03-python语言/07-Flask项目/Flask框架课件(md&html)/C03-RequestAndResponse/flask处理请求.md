# 处理请求

> 在视图编写中需要读取客户端请求携带的数据时，如何才能正确的取出数据呢？
>
> 请求携带的数据可能出现在HTTP报文中的不同位置，需要使用不同的方法来获取参数。
>
> - URL路径参数（动态路由）
>   - URL路径参数的其他类型
>   - 自定义URL路径参数的类型
> - 查询字符串
> - 请求体

[TOC]
<!-- toc -->

## 1. URL路径参数(动态路由)

> 例如，有一个请求访问的接口地址为`/users/123`，其中`123`实际上为具体的请求参数，表明请求123号用户的信息。此时如何从url中提取出123的数据？
>
> Flask不同于Django直接在定义路由时编写正则表达式的方式，而是采用转换器语法：

### 1.1 基本用法

> ```python
> from flask import Flask
> app = Flask(__name__)
> 
> # 此处的<user_id>即是一个转换器，默认为字符串类型，即将该位置的数据以字符串格式进行匹配、并以字符串为数据类型类型、 user_id为参数名传入视图。
> @app.route('/users/<user_id>')
> def get_user_id(user_id):
>     print(type(user_id))
>     return 'hello user {}'.format(user_id)
> 
> if __name__ == '__main__':
>     app.run(debug=True)
> ```

### 1.2 URL路径参数的其他类型

> - 在刚才的案例中， URL路径参数默认是str类型的，Flask也提供其他类型的转换器：
>
>   > ```python
>   > DEFAULT_CONVERTERS = {
>   >  'default':          UnicodeConverter,
>   >  'string':           UnicodeConverter,
>   >  'any':              AnyConverter,
>   >  'path':             PathConverter,
>   >  'int':              IntegerConverter,
>   >  'float':            FloatConverter,
>   >  'uuid':             UUIDConverter,
>   > }
>   > ```
>
> -  URL路径参数类型的转换器的具体使用
>
>   > ```python
>   > from flask import Flask
>   > app = Flask(__name__)
>   > 
>   > # http://127.0.0.1:5000/users/123
>   > @app.route('/users/<int:user_id>')
>   > def user_info(user_id):
>   >     print(type(user_id))
>   >     return 'hello user: {}'.format(user_id)
>   > 
>   > # http://127.0.0.1:5000/path/a/b/c
>   > @app.route('/path/<path:path_str>')
>   > def path_info(path_str):
>   >     print(type(path_str)) # str
>   >     return 'hello path: {}'.format(path_str) # hello path: a/b/c
>   > 
>   > if __name__ == '__main__':
>   >     app.run(debug=True)
>   > ```

### 1.3 自定义URL路径参数的类型转换器

> 如果遇到需要严格匹配提取`/sms_codes/18512345678`中的手机号数据，Flask内置的转换器就无法满足需求，此时需要自定义转换器。
>
> ```python
> from flask import Flask
> from werkzeug.routing import BaseConverter
> 
> app = Flask(__name__)
> 
> # step 1. 创建转换器类，保存匹配时的正则表达式
> # 注意regex名字固定
> class MobileConverter(BaseConverter):
>     """手机号格式"""
>     regex = r'1[3-9]\d{9}'
> # step 2. 将自定义转换器添加到转换器字典中，并指定转换器使用时名字为: mobile
> app.url_map.converters['mobile'] = MobileConverter
> # step 3. 在使用转换器的地方定义使用
> @app.route('/mobile/<mobile:mob_num>')
> def send_sms_code(mob_num):
>     return 'mobile is: {}'.format(mob_num)
> 
> if __name__ == '__main__':
>     app.run(debug=True)
> ```
>
> - 测试：
>
>   > `http://127.0.0.1:5000/mobile/13161933359` 正常返回
>   >
>   > `http://127.0.0.1:5000/mobile/1316193` 返回404
>   >
>   > - 思考：为什么第二个url返回404？
>   >   - 自定义的转换器类，本质是把url的格式固定死了。

## 2. 查询字符串

> `http://127.0.0.1:5000/s?a=1&b=2` ，url中`?`后边，以`=`连接键值对后，再以`&`连接的部分就是查询字符串部分。
>
> - 使用`Flask.request.args`来获取查询字符串
> - `Flask.request`是flask封装提供的请求对象
>
> ```python
> from flask import Flask, request
> app = Flask(__name__)
> 
> @app.route('/s')
> def index():
>     args_list = request.args.lists()
>     for arg in args_list:
>         print(arg)
>     print(request.args.to_dict())
>     print(request.args.get('a'))
>     print(request.args.get('b', '没有b'))
>     return request.args['a']
> 
> if __name__ == '__main__':
>     app.run(debug=True)
> ```
>
> `http://127.0.0.1:5000/s?a=1&a=2`试一试

## 3. 请求体

> POST请求存在四种请求体，前三种比较常见，他们都出现在请求头中的`Content-Type`中
>
> - application/x-www-from-urlencoded
> - application/json
> - multipart/form-data
> - text/xml

### 3.1 POST `application/x www from urlencoded`

> 使用`Flask.request.form`
>
> ```python
> from flask import Flask, request
> app = Flask(__name__)
> 
> @app.route('/post_data', methods=['POST'])
> def post_data():
>     # application/x-www-form-urlencoded
>     print(request.form)
>     print(request.form['a'])
>     return request.form.get('b')
> 
> if __name__ == '__main__':
>     app.run(debug=True)
> ```
>
> - 测试代码
>
>   > ```python
>   > import requests
>   > # application/x-www-form-urlencoded格式
>   > data_dict = {"a": "1", "b": "2"}
>   > r = requests.post("http://127.0.0.1:5000/post_data", data=data_dict)
>   > print(r.text)
>   > print(r.status_code)
>   > ```

### 3.2 POST `application/json`

> 使用`Flask.request.data` 或 `Flask.request.json`
>
> ```python
> from flask import Flask, request
> app = Flask(__name__)
> 
> @app.route('/post_json', methods=['POST'])
> def post_json():
>     print(request.data)
>     print(request.json)
>     return request.data.decode()
>     
> if __name__ == '__main__':
>     app.run(debug=True)
> ```
>
> - 测试代码
>
>   > ```python
>   > import requests, json
>   > headers = {'Content-Type': 'application/json'}
>   > datas = json.dumps({"a": "1", "b": "2"})
>   > r = requests.post("http://127.0.0.1:5000/post_json", data=datas, headers=headers)
>   > print(r.text)
>   > ```

### 3.3 POST `multipart/form data`

> 我们来演示一下用`multipart/form-data`格式发送post请求**上传文件**
>
> ```python
> from flask import Flask, request
> app = Flask(__name__)
> 
> @app.route('/upload', methods=['POST'])
> def upload_file():
>     f = request.files['zidingyi_name']
>     f.save('./4_1_3_upload.py')
>     # with open('./demo.png', 'wb') as new_file:
>     #     new_file.write(f.read())
>     return 'ok'
> 
> if __name__ == '__main__':
>     app.run(debug=True)
> ```
>
> - 测试代码
>
>   > ```python
>   > import requests
>   > files = {"zidingyi_name": open("./4_1_3.py", "rb")}
>   > r = requests.post("http://127.0.0.1:5000/upload", files=files)
>   > print(r.text)
>   > ```
>
> - 思考：图片怎么上传？

### 3.4 拓展:发送`text/xml`请求

> Flask视图中可以使用request.data来获取text/xml形式的请求体，这里就不做演示了
>
> ```python
> import requests
> headers = {"Content-Type": "text/xml"}
> datas = """<?xml version="1.0"?>
> <methodCall>
>     <methodName>examples.getStateName</methodName>
>     <params>
>         <param>
>             <value><i4>41</i4></value>
>         </param>
>     </params>
> </methodCall>"""
> r = requests.post("http://httpbin.org/post", data=datas, headers=headers)
> print(r.text)
> ```

- 拓展阅读:[postman的使用](https://segmentfault.com/a/1190000014343759?utm_source=tag-newest)

## 4. 其他参数[查表]

> `Flask.request`还有其他参数，现将常用的列表如下：
>
> | 属性    | 说明                           | 类型           |
> | :------ | :----------------------------- | :------------- |
> | data    | 记录请求的数据，并转换为字符串 | \*             |
> | form    | 记录请求中的表单数据           | MultiDict      |
> | args    | 记录请求中的查询参数           | MultiDict      |
> | cookies | 记录请求中的cookie信息         | Dict           |
> | headers | 记录请求中的报文头             | EnvironHeaders |
> | method  | 记录请求使用的HTTP方法         | GET/POST       |
> | url     | 记录请求的URL地址              | string         |
> | files   | 记录请求上传的文件             | \*             |





