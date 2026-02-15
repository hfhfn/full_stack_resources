# Supervisor

> supervisor是进程管理工具

[TOC]

<!-- toc -->

## 1. 安装

> - **supervisor对python3支持不好，须使用python2**
>
> centos测试开发虚拟机已安装
>
> ```shell
> pip -V # 查看并确认pip为python2版本
> sudo pip install supervisor # 直接在默认环境下安装（非虚拟环境）
> ```

## 2. 配置

### 2.1 创建默认`supervisord.conf`配置文件

> 运行**echo\_supervisord\_conf**命令输出默认的配置项，可以如下操作将默认配置保存到文件中
>
> ```shell
> ssh root@192.168.45.128
> cd /home/python
> # echo_supervisord_conf命令输出默认的配置项 重定向到suoervisord.conf文件中
> echo_supervisord_conf > supervisord.conf # 可以在任意路径下执行
> ```

### 2.2 修改默认`supervisord.conf`配置文件

> ```shell
> sudo vi supervisord.conf
> # 在supervisord.conf文件的最后，把
> ;[include]
> ;files = relative/directory/*.ini
> # 改为
> [include]
> files = /etc/supervisor/*.conf
> # include选项指明包含的其他配置文件
> ```

### 2.3 移动默认配置文件

> ```shell
> # 将编辑后的supervisord.conf文件复制到/etc/目录下
> sudo cp supervisord.conf /etc/
> ```

### 2.4 创建并完成`supervisor`项目配置文件

#### 2.4.1 创建`supervisor`项目配置文件

> ```shell
> # 创建/etc/supervisor文件夹
> cd /etc
> sudo mkdir supervisor
> cd supervisor
> # 创建/etc/supervisor/toutiao.conf文件
> sudo vi toutiao.conf
> # 给/etc/supervisor/toutiao.conf文件添加可执行权限
> sudo chmod +x toutiao.conf
> ```

#### 2.4.2 完成`supervisor`项目配置文件

> ```python
> [group:toutiao]
> programs=toutiao-app
> 
> [program:toutiao-app]
> command=/home/python/toutiao-backend/scripts/toutiao_app.sh
> directory=/home/python/toutiao-backend
> user=python
> autorestart=false
> redirect_stderr=false
> stdout_logfile=/home/python/logs/s-app.log
> stderr_logfile=/home/python/logs/s-e-app.log 
> loglevel=info
> stopsignal=KILL
> stopasgroup=true
> killasgroup=true
> ```
>
> - 解释说明
>
>   > ```shell
>   > [group:toutiao] #组名字                                                    
>   > programs=toutiao-app # 组里应用的名字 
>   > [program:toutiao-app] # 应用的名字
>   > # 通过哪个脚本来启动指定的应用
>   > command=/home/python/toutiao-backend/scripts/toutiao_app.sh 
>   > directory=/home/python/toutiao-backend  # 程序的目录
>   > user=python  # 启动的用户
>   > autorestart=false  # 是否自动重启，轻易不要设置为true！
>   > redirect_stderr=false  # 出错后是否写入Supervisor专门的日志
>   > loglevel=info  # Supervisor的日志级别
>   > stdout_logfile=/home/python/logs/s-app.log # 标准输出日志   
>   > stderr_logfile=/home/python/logs/s-e-app.log # 异常输出日志
>   > stopsignal=KILL  # stop操作使用的命令
>   > stopasgroup=true  # 停止进程时, 是否一起停止其子进程
>   > ```

## 3. 启动`supervisord`服务

> ```shell
> supervisord -c /etc/supervisord.conf
> ```

## 4. 异常处理

### 4.1 处理supervisord服务进程的方法

> ```shell
> # 查看supervisord服务的进程号
> ps aux | grep supervisord 
> # 杀进程
> sudo kill -9 xxxx 
> # 移除supervisord进程锁，如果不移除，将无法再次启动supervisord服务
> sudo unlink /tmp/supervisor.sock 
> ```

### 4.2 无法正常启动`toutiao`项目的常见问题

> ```shell
> # 通过该命令查看异常日志，从而定位问题进行解决
> tail -n 100 /home/python/logs/s-e-app.log
> ```
>
> - 没有logs文件夹
>
>   > ```shell
>   > cd /home/python
>   > mkdir logs
>   > ```
>   >
>   > dsd
>
> - 没有权限
>
>   > ```shell
>   > # 直接设置整个用户目录的权限 不推荐这么做
>   > sudo chmod -R 777 /home/python
>   > ```
>
> - 无法启动supervisord服务
>
>   > ```shell
>   > # 移除supervisord服务进程的锁文件连接
>   > unlink  /tmp/supervisor.sock
>   > ```
>
> - web服务能够访问，但supervisorctl中看到的服务状态却是异常的
>
>   > ```shell
>   > # 修改/home/python/toutiao-backend/scripts/toutiao_app.sh中的
>   > # exec gunicorn -preload -w 2 --threads 5 -b 0.0.0.0:8000 --access-logfile /home/python/logs/access_app.log --error-logfile /home/python/logs/error_app.log toutiao.main:app
>   > # 删除-preload 修改为
>   > exec gunicorn -w 2 --threads 5 -b 0.0.0.0:8000 --access-logfile /home/python/logs/access_app.log --error-logfile /home/python/logs/error_app.log toutiao.main:app
>   > ```
>
> - gunicorn设置了`-w 3`，但supervisord启动之后，用`ps aux | grep python`看到不是3个pythonweb进程，进程数量对不上
>
>   > - 是因为在`supervisord的toutiao.conf`配置文件设置了`autorestart=true  # 是否自动重启`
>   >
>   > - 一旦supervisord的服务启动了，就会自动恢复pythonweb进程
>   > - 所以，`autorestart`尽量不要设置为true！

## 5. 使用`supervisorctl`控制进程

> 像redis一样，supervisor也分服务端和客户端；我们可以利用supervisorctl来进入客户端终端，进而管理supervisord服务控制的进程
>
> ```shell
> supervisorctl # 进入supervisor客户端
> 
> status    # 查看程序状态
> start toutiao:toutiao-app  # 启动 单一程序
> stop toutiao:*   # 关闭 toutiao组 程序
> start toutiao:*  # 启动 toutiao组 程序
> restart toutiao:*    # 重启 toutiao组 程序
> update    # 重启配置文件修改过的程序
> 
> # 执行status命令时，显示如下信息说明程序运行正常：
> supervisor> status
> toutiao:toutiao-app RUNNING pid 32091, uptime 00:00:02
> ```



