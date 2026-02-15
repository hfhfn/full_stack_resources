# 处理响应

> - 如何在不同的场景里返回不同的响应信息？
>   - 模板
>   - 重定向
>   - 返回JSON
>   - 自定义状态码和响应头

[TOC]
<!-- toc -->

## 1. 返回模板

> flask中集成了jinja2模板，在视图函数中，使用`render_template`方法渲染模板并返回
>
> - 例如，新建一个模板index.html
>
> ```html
> <!DOCTYPE html>
> <html lang="en">
> <head>
>     <meta charset="UTF-8">
>     <title>Title</title>
> </head>
> <body>
> 我的模板html内容
> <br/>{{ my_str }}
> <br/>{{ my_int }}
> </body>
> </html>
> ```
>
> - 后端视图
>
> ```python
> from flask import Flask, render_template
> app = Flask(__name__)
> 
> @app.route('/')
> def index():
>     mstr = 'Hello 黑马程序员'
>     mint = 10
>     return render_template('index.html', my_str=mstr, my_int=mint)
> 
> if __name__ == '__main__':
>     app.run()
> ```

## 2.  重定向

> 跳转其他url
>
> ```python
> from flask import Flask, redirect
> app = Flask(__name__)
> 
> @app.route('/demo2')
> def demo2():
>     return redirect('http://www.itheima.com')
> 
> if __name__ == '__main__':
>     app.run()
> ```

## 3. 返回JSON

> ```python
> from flask import Flask, jsonify
> app = Flask(__name__)
> 
> @app.route('/demo3')
> def demo3():
>     json_dict = {
>         "user_id": 10,
>         "user_name": "laowang"
>     }
>     return jsonify(json_dict)
> 
> if __name__ == '__main__':
>     app.run()
> ```

## 4. 自定义状态码和响应头

### 4.1 元祖方式

> 视图函数可以返回一个元组，这样的元组必须是 **(response, status, headers)** 的形式，且至少包含一个元素。 status 值会覆盖状态代码， headers 可以是一个列表或字典，作为额外的消息标头值。
>
> ```python
> @app.route('/demo4')
> def demo4():
>     # return '状态码为 666', 666
>     # return '状态码为 666', 666, [('Itcast', 'Python')]
>     return '状态码为 666', 666, {'Itcast': 'Python'}
> ```
>
> ![4-2-4-1](..\images\4-2-4-1.png)

### 4.2 make_response方式

> flask.make_response函数构造response响应对象
>
> ```python
> @app.route('/demo5')
> def demo5():
>     resp = make_response('make response测试')
> 		resp.headers[“Itcast”] = “Python2”
> 		resp.status = “404 not found”
>     return resp
> ```
>
> ![4-2-4-2](..\images\4-2-4-2.png)

