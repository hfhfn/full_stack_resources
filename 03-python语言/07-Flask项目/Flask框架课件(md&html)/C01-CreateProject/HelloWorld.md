# Flask的HelloWorld

[TOC]
<!-- toc -->

## 1. Flask程序编写

> 创建helloworld.py文件
>
> ```python
> # 导入Flask类
> from flask import Flask
> 
> #Flask类接收一个参数__name__
> app = Flask(__name__)
> 
> # 装饰器的作用是将路由映射到视图函数index
> @app.route('/')
> def index():
>     return 'Hello World'
> 
> # Flask应用程序实例的run方法启动WEB服务器
> if __name__ == '__main__':
>     app.run()
> ```

## 2. 启动运行

> - 命令行终端用python解释器运行
>
>   > 切换至虚拟环境中执行
>
>   ```shell
>   workon venv_name
>   python helloworld.py
>   ```
>
> - pycharm 运行
>
>   像正常运行普通python程序一样即可。
>
> - 命令行终端用flask命令运行
>
>   ```shell
>   workon venv_name # 切入虚拟环境
>   export FLASK_APP=helloworld # 设置环境变量
>   flask run -h 0.0.0.0 -p 5000 # 启动
>   ```