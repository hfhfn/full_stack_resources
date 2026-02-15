# Gunicorn的使用

> Gunicorn（绿色独角兽）是一个Python WSGI的HTTP服务器。从Ruby的独角兽（Unicorn ）项目移植。该Gunicorn服务器与各种Web框架兼容，实现非常简单，轻量级的资源消耗。Gunicorn直接用命令启动，不需要编写配置文件，相对uWSGI要容易很多。

[TOC]

<!-- toc -->

## 1. 安装gunicorn

> 可以安装到python虚拟环境中，centos测试开发虚拟机已经安装过了
>
> ```shell
> pip install gunicorn
> ```

## 2. 查看命令行选项

> 安装gunicorn成功后，通过命令行的方式可以查看gunicorn的使用信息。
>
> ```shell
> gunicorn -h
> ```

## 3. 使用gunicorn启动flask

### 3.1 直接运行

> 不推荐使用该方式
>
> ```shell
> #直接运行，默认启动的127.0.0.1::8000
> gunicorn 运行文件名称:Flask程序实例名
> ```

### 3.2 指定进程和端口号

> ```shell
> source /home/python/.virtualenv/toutiao/bin/activate
> cd /home/python/toutiao-backend
> gunicorn -w 4 --threads 10 -b 0.0.0.0:5001 toutiao.main:app
> ```
>
> - `-w 4` 进程数量
> - `-threads 10` 线程数量 
> - `-b 0.0.0.0:5001` 绑定ip:port 
> - `toutiao.main:app` 运行文件的名称:flask_app的实例化对象名字

#### 3.3 设置gunicorn的访问日志和错误日志

> ```shell
> source /home/python/.virtualenv/toutiao/bin/activate
> cd /home/python/toutiao-backend
> gunicorn -w 4 --threads 10 -b 0.0.0.0:5001 --access-logfile /home/python/logs/access_app.log --error-logfile /home/python/logs/error_app.log toutiao.main:app
> ```
>
> - `--access-logfile` 访问日志路径
> - `--error-logfile` 错误日志路径
> - 注意：这里设置的gunicorn的日志路径，跟flask的日志没有关系！

## 4. 注意

> - 如果使用gunicorn来启动web应用, 首先执行的文件不是main.py, 而是`toutiao/__init.py`
> - ip不能设为`127.0.0.1`
> - `--error-logfile`和 `--access-logfile` 设置的gunicorn的日志 和flask的日志无关
> - `-w 4 --threads 10`表示开启4个进程，每个进程开启10个线程



