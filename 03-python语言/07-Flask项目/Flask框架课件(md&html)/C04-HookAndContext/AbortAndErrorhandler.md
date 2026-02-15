# 异常处理

[TOC]
<!-- toc -->

## 1. HTTP异常主动抛出

> - abort 方法
>   - 抛出一个给定状态代码的 HTTPException 或者 指定响应，例如想要用一个页面未找到异常来终止请求，你可以调用 abort(404)。
> - 参数：
>   - code – HTTP的错误状态码
>
> ```python
> # abort(404)
> abort(500)
> ```
>
> 抛出状态码的话，只能抛出 HTTP 协议的错误状态码

## 2. 捕获错误

> - errorhandler 装饰器
> - 注册一个错误处理程序，当程序抛出指定错误状态码的时候，就会调用该装饰器所装饰的方法
> - 参数：
>   - code_or_exception – HTTP的错误状态码或指定异常
> - 例如统一处理状态码为500的错误给用户友好的提示：
>
> ```python
> @app.errorhandler(500)
> def internal_server_error(e):
>     return '服务器搬家了'
> ```
>
> - 捕获指定异常
>
> ```python
> @app.errorhandler(ZeroDivisionError)
> def zero_division_error(e):
>     return '除数不能为0'
> ```

## 3. 完整示例代码解读

> ```python
> from flask import Flask, abort
> 
> app = Flask(__name__)
> 
> # app.errorhandler 可以捕获http错误 和 系统内置错误
> @app.errorhandler(404) # 捕获http-404错误
> def eror_404(e): # 必须接收异常信息参数
>     return '走丢了！ 404 ' # 一旦触发捕获的异常给前端返回的内容
> 
> @app.route('/404')
> def index1():
>     abort(404) # 主动抛出http异常，被@app.errorhandler(404)捕获了异常
>     return 'heihei'
> 
> @app.route('/500')
> def index2():
>     abort(500) # 主动抛出http异常，
>     return
> 
> @app.errorhandler(ZeroDivisionError) # 捕获系统内置错误
> def error_zero(e):
>     return '除数真的不能为0'
> 
> @app.route('/0')
> def index3():
>     1 / 0 # 强行造的异常
>     return '除数不能为0' 
> 
> if __name__ == '__main__':
>     app.run(debug=True)
> ```