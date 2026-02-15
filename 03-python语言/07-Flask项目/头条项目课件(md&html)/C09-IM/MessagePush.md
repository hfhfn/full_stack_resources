# 头条在线消息推送实现

[TOC]

<!-- toc -->

## 1. 需求

> 产品原型图中，我的-消息通知，需要我们实现**在头条的Flask应用中，用户关注后需要推送消息，通过消息队列告知IM服务为用户进行推送**，下图就是实现需求的流程，为了学习推送的实现，第2步写入数据库就不去实现了。
>
> ![push](../images/推送关注通知流程.png)

## 2. 分析和代码实现的步骤

> 因为要给指定的用户推送消息，所以需要用到用户的身份，用户在客户端携带JWT连接SocketIO服务器，我们在IM服务器端对jwt token进行验证，对于验证出用户身份(user_id)的客户端，将其添加到名为用户user_id的room房间中，方便按照user_id进行推送。

### 2.1 视图函数分析

> 在`toutiao-backend/toutiao/resources/user/__init__.py`中已经规定了路由

#### 2.1.1 接口规定

> - 请求方式：`POST /v1_0/user/followings`
> - 请求参数：`target` `int` 被关注用户的`user_id`
> - 返回 `{target}`

#### 2.1.2实现步骤

> - 使用`login_required装饰器`进行用户认证
>
> - 解析请求参数，获取被关注用户的user_id
>
>   ```python
>   json_parser = RequestParser()
>   json_parser.add_argument('target', type=int, required=True, location='json')
>   args = json_parser.parse_args()
>   target = str(args.target)
>   ```
>
> - 通知socketio服务，把发起关注的A用户和被关注的B用户的user_id写入消息队列
>
>   - 构造发送的消息`{发起关注的A用户的user_id, 时间戳}`
>
>   - `规定事件名称，以被关注用户的user_id作为room，构造的消息`——把上述整体通知发送给消息队列
>
>     ```python
>     # 在toutiao-backend/toutiao/__init__.py中创建sio的队列管理器对象，一旦设置flaskapp运行必须为生产模式
>     # sio队列管理器 socketio.KombuManager必须安装kombu模块
>     # pip install kombu
>     # app.config['RABBITMQ']使用了rabbitmq作为消息队列，sio队列管理器也可以使用redis作为消息队列
>     app.sio_maneger = socketio.KombuManager(app.config['RABBITMQ'], write_only=True)
>     # 在视图中用sio的队列管理器向用户个人房间发送规定名称的事件消息，消息内容包含了关注者的user_id
>     # 将‘把Auser_id，发送给名为Buser_id的房间，事件是following notify’整体放入消息队列
>     # sio服务就可以从消息队列中把该信息取出，并执行，向Buser_id发送消息为把Auser_id的名为following notify的事件
>     current_app.sio_maneger.emit('following notify', data=_data, room='Buser_id')
>     ```
>
> - 最终返回 `{target}`

### 2.2 socketio服务分析

#### 2.2.1 创建sio应用对象

> - 创建消息队列管理器，构建能够sio服务对象，并设置消息队列管理器对象做为client_manager的参数
>
>   ```python
>   # 创建sio服务端的消息管理器
>   mgr = socketio.KombuManager(RABBITMQ_url)
>   # 创建sio对象
>   sio = socketio.Server(async_mode='eventlet', client_manager=mgr)
>   ```
>
>   - sio服务就会从消息队列中取出flask web视图的消息，进而把关注信息发送给指定的room（被关注用户的user_id）

#### 2.2.2 完成事件处理方法

> - connect
>
>   > - 从environ参数中取出token，再反序列化取出连接sio服务的用户的user_id
>   >
>   >   ```python
>   >    # 利用werkzeug模块从请求对象的参数中取出token字段的值
>   >    JWtoken = werkzeug.wrappers.Request(environ).args.get('token')
>   >    # 利用jwt模块对JWtoken按secret进行反序列化，并取出user_id
>   >    user_id = jwt.decode(JWtoken, secret, algorithm=['HS256'])['user_id']
>   >    # 把建立连接的用户添加到他自己对应的以其自身user_id命名的房间
>   >    sio.enter_room(sid, str(user_id))
>   >   ```
>   >
>   >   - 规定客户端向服务端建立连接的请求必须携带JWToken作为参数
>   >   - 规定客户端必须监听flask web规定的事件
>   >
>   > - 把该用户添加到以他自己的user_id命名的room
>
> - disconnect
>
>   > - 把用户移除他自己的room
>   >
>   >   ```python
>   >    rooms = sio.rooms(sid)
>   >    for room in rooms: # 移出所有房间
>   >        sio.leave_room(sid, room)
>   >   ```
>

#### 2.2.3 启动socketio服务器

> - 获取sio服务的端口
>
> - 创建监听对象
>
> - 以eventlet.wsgi提供的的方式运行
>
> ```python
> if len(sys.argv) < 2: port = 8090
> else: port = int(sys.argv[1])
> app = socketio.Middleware(sio)
> sock = eventlet.listen(('', port))
> eventlet.wsgi.server(sock, app)
> ```

### 2.3 运行逻辑的流程图

> ![](../images/9-4-1.png)



## 3. 测试运行

### 3.1 完成测试代码

> - 测试运行步骤
>
>   > - A登录获取A token
>   > - B登录获取B token
>   > - 使用Firecamp设置请求参数为`token=B token`，监听`following notify`，与IM服务端建立连接
>   > - A携带token向web关注视图发送关注B的请求
>
> - 测试代码
>
>   > 在`Test/test_f_sio/test_sio.py`中
>   >
>   > ```python
>   > import requests, json, jwt
>   > from redis.sentinel import Sentinel
>   > 
>   > REDIS_SENTINELS = [('127.0.0.1', '26380'),
>   >                    ('127.0.0.1', '26381'),
>   >                    ('127.0.0.1', '26382'),]
>   > REDIS_SENTINEL_SERVICE_NAME = 'mymaster'
>   > _sentinel = Sentinel(REDIS_SENTINELS)
>   > redis_master = _sentinel.master_for(REDIS_SENTINEL_SERVICE_NAME)
>   > 
>   > """A用户登录"""
>   > redis_master.set('app:code:18911111111', '123456')
>   > # 构造raw application/json形式的请求体
>   > data = json.dumps({'mobile': '18911111111', 'code': '123456'})
>   > # requests发送 POST raw application/json 登录请求
>   > url = 'http://192.168.45.128:5000/v1_0/authorizations'
>   > resp = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
>   > """获取A用户token"""
>   > # 从登录请求的响应中获取token
>   > a_token = resp.json()['data']['token']
>   > # print(a_token)
>   > 
>   > """B用户登录"""
>   > redis_master.set('app:code:13911111111', '123456')
>   > # 构造raw application/json形式的请求体
>   > data = json.dumps({'mobile': '13911111111', 'code': '123456'})
>   > # requests发送 POST raw application/json 登录请求
>   > url = 'http://192.168.45.128:5000/v1_0/authorizations'
>   > resp = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
>   > """获取B用户token"""
>   > # 从登录请求的响应中获取token
>   > b_token = resp.json()['data']['token']
>   > print('{}'.format(b_token))
>   > """获取B用户的user_id"""
>   > secret = 'TPmi4aLWRbyVq8zu9v82dWYW17/z+UvRnYTt4P6fAXA'
>   > b_user_id = jwt.decode(b_token, secret, algorithm=['HS256'])['user_id']
>   > print(b_user_id)
>   > # print(type(b_user_id))
>   > 
>   > """"""
>   > input('这个时候请用Firecamp，向query中添加B用户的token，字段是token，连接sio服务，用户监听following notify')
>   > 
>   > """发送关注请求 A关注B"""
>   > # 构造请求头：带着token发送请求
>   > headers = {'Authorization': 'Bearer {}'.format(a_token),
>   >            'Content-Type': 'application/json'}
>   > url = 'http://192.168.45.128:5000/v1_0/user/followings'
>   > data = json.dumps({'target': b_user_id})
>   > resp = requests.post(url, headers=headers, data=data)
>   > print(resp.json()) # 打印获取关注结果
>   > ```

### 3.2 配合使用Firecamp插件

> ![关注推送效果](../images/用户关注推送.png)

## 4. 完整代码

### 4.1 在web中添加路由并设置消息队列管理器

> - 在`toutiao/__init__.py`中设置消息队列管理器
>
> ```python
>     ...
>     # socket.io
>     app.sio_maneger = socketio.KombuManager(app.config['RABBITMQ'], write_only=True)
> 	...
> ```
>
> - 在`toutiao/resources/user/__init__.py`中添加路由
>
> ```python
> ...
> user_api.add_resource(following.FollowingListResource, '/v1_0/user/followings',
>                       endpoint='Followings')
> ...
> ```

### 4.2 发送关注请求的视图函数

> 在`toutiao/resources/user/following.py`中
>
> ```python
> from flask_restful import Resource
> from flask_restful.reqparse import RequestParser
> from flask import g, current_app
> import time
> 
> from utils.decorators import login_required
> from utils import parser
> 
> 
> class FollowingListResource(Resource):
>     method_decorators = [login_required]
> 
>     def post(self):
>         """关注用户 发送关注通知"""
>         json_parser = RequestParser()
>         json_parser.add_argument('target', type=int,
>                                  required=True, location='json')
>         args = json_parser.parse_args()
>         target = args.target
> 
>         # 发送关注通知
>         _data = {
>             'user_id': g.user_id,
>             'timestamp': int(time.time())
>         }
>         current_app.sio_maneger.emit('following notify',
>                              data=_data, room=str(target))
> 
>         return {'target': target}
> ```

### 4.3 IM服务端代码

> 在`im/main.py`中
>
> ```python
> import eventlet
> eventlet.monkey_patch()
> 
> import jwt
> import sys
> import socketio
> import eventlet.wsgi
> from werkzeug.wrappers import Request
> 
> JWT_SECRET = 'TPmi4aLWRbyVq8zu9v82dWYW17/z+UvRnYTt4P6fAXA'
> RABBITMQ = 'amqp://python:rabbitmqpwd@localhost:5672/toutiao'
> mgr = socketio.KombuManager(RABBITMQ)
> # 创建sio对象
> sio = socketio.Server(async_mode='eventlet', client_manager=mgr)
> 
> """定义事件处理方法"""
> @sio.on('connect')
> def on_connect(sid, environ): # 与客户端建立连接后执行
>     request = Request(environ)  # werkzeug.wrappers.Request
>     token = request.args.get('token') # 从请求的查询字符串中取出JWToken
>     # token反序列化，取出user_id
>     user_id = jwt.decode(token, JWT_SECRET,
>                          algorithm=['HS256'])['user_id']
>     # 将新连接的客户端添加到名为user_id的room中
>     sio.enter_room(sid, str(user_id))
> 
> @sio.on('disconnect')
> def on_disconnect(sid): # 与客户端断开连接时执行 将客户端从所有房间中移除
>     rooms = sio.rooms(sid)
>     for room in rooms:
>         sio.leave_room(sid, room)
> 
> """通过命令行启动sio服务，并通过命令行指定端口"""
> # 获取命令行参数，目的是想让im服务运行的端口在启动程序时指定
> if len(sys.argv) < 2: exit(1)  # 如果收到的参数小于2 退出当前进程
> SERVER_ADDRESS = ('', int(sys.argv[1])) # socketio服务器运行的地址
> # 启动socketio服务器
> app = socketio.Middleware(sio)
> sock = eventlet.listen(SERVER_ADDRESS)
> eventlet.wsgi.server(sock, app)
> ```



## 5. 发散思考

### 5.1 RPC和消息队列的选择

> 为什么要选择使用消息队列而不使用RPC呢？
>
> - 需要子系统立即返回结果的场景，必须使用RPC
> - 不需要子系统返回结果立即响应的场景，可以是用消息队列，起到通知的作用

### 5.2 用户上线收到通知的逻辑

> 用户下线时候被关注了，这种情况代码实现逻辑应该怎么做？
>
> - 用户一旦连接IM
>   - 需要让user_id和sid建立关系
>   - 一旦离线就删除关系
>   - 关系可以存在redis中
> - web系统
>   - 从redis中取user_id对应的sid
>   - 如果能取出, 说明在线, 直接往消息队列中添加消息
>   - 如果不能取出, 说明离线, 将消息保存到redis中
> - im服务端
>   - 一旦建立连接, 先从redis中查询是否有消息被保存
>   - 如果有, 取出并发给客户端, 取出后从redis中删除数据
>   - 同时还需要从消息队列中实时取出消息数据



