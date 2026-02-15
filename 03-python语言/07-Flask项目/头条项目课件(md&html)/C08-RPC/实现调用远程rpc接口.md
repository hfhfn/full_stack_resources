# 课后练习：实现调用远程rpc接口

> 一定要努力尝试完成哦！

[TOC]

<!-- toc -->

## 1. 需求

> - 用前几小节完成的grpc server的代码作为rpc的远程服务
>
> - 接口信息
>
>   > - GET /v1_0/articles
>   >
>   > - HEADERS 
>   >
>   >   > - Content-Type application/json
>   >   > - Authorization Bearer eyJ0eX... （温馨提示：可以通过g对象取出user_id）
>   >
>   > - QUERY
>   >
>   >   > - channel_id 频道ID
>   >   > - time_stamp 推荐的时间戳，不传默认为当前
>   >   > - article_num 要求返回文章id的数量，不传数量由后端决定
>   >
>   > - RESPONSE DATA
>   >
>   >   > - expousre  曝光埋点数据 str类型
>   >   >
>   >   > - time_stamp 推荐的时间戳 单位秒 int类型
>   >   >
>   >   > - recommends 推荐结果 list
>   >   >
>   >   >   > - article_id 文章id int类型
>   >   >   >
>   >   >   > - track 关于文章的埋点数据
>   >   >   >
>   >   >   >   > - click 用户点击行为的埋点参数 str类型
>   >   >   >   > - collect 用户收藏的埋点参数 str类型
>   >   >   >   > - share 用户分享的埋点参数 str类型
>   >   >   >   > - read 用户进入文章详情的埋点参数 str类型   

## 2. 按步骤实现代码

### 2.1 完成视图类

> 在 `/toutiao/resources/news/`新建 `article.py` ，完成视图
>
> ```python
> import time
> import grpc
> from flask import g
> from flask_restful import Resource
> from flask_restful.reqparse import RequestParser
> from utils.decorators import login_required
> from rpc import reco_pb2, reco_pb2_grpc
> 
> 
> class ArticleListResource(Resource):
> 
>     method_decorators = [login_required]
> 
>     def _get_rpc_article_list(self, stub,
>                               user_id,
>                               channel_id:int,
>                               time_stamp=round(time.time()*1000),
>                               article_num=10):
>         # 构建rpc调用的调用参数
>         user_request = reco_pb2.UserRequest()  # 实例化请求参数对象 对应proto文件中的UserRequest
>         user_request.user_id = str(user_id)
>         user_request.channel_id = channel_id
>         user_request.article_num = article_num
>         user_request.time_stamp = time_stamp
> 
>         # 通过stub进行方法调用，并接收调用返回值
>         rpc_ret = stub.user_recommend(user_request)  # 对应proto文件中的user_recommend函数
>         print(rpc_ret)
>         print(rpc_ret.recommends[0].track.click)
>         return rpc_ret
> 
>     def get(self):
>         # 获取参数
>         parser = RequestParser()
>         parser.add_argument('channel_id', location='args', type=int, required=True, help='频道id int')
>         args = parser.parse_args()
>         # 远程调用推荐系统的函数
>         # 使用with语句连接rpc服务器
>         with grpc.insecure_channel('127.0.0.1:8888') as channel:
>             # 创建调用rpc远端服务的辅助对象stub
>             stub = reco_pb2_grpc.UserRecommendStub(channel)
>             # 通过stub进行rpc调用
>             rpc_resp = self._get_rpc_article_list(stub, g.user_id, args.channel_id)
> 
>         # 构造数据并返回
>         recommends = []
>         for article in rpc_resp.recommends:
>             article_dict = {}
>             article_dict['article_id'] = article.article_id
>             article_dict['track'] = dict()
>             article_dict['track']['click'] = article.track.click
>             article_dict['track']['collect'] = article.track.collect
>             article_dict['track']['share'] = article.track.share
>             article_dict['track']['read'] = article.track.read
>             recommends.append(article_dict)
> 
>         return {
>             'expousre': rpc_resp.expousre,
>             'time_stamp': rpc_resp.time_stamp,
>             'recommends': recommends
>         }
> ```

### 2.2 构建蓝图

> 在 `/toutiao/resources/news/__init__.py`完成代码
>
> ```python
> from flask import Blueprint
> from flask_restful import Api
> 
> from utils.output import output_json
> from . import article
> 
> news_bp = Blueprint('news', __name__)
> news_api = Api(news_bp, catch_all_404s=True)
> news_api.representation('application/json')(output_json) # 前者返回一个函数
> 
> news_api.add_resource(article.ArticleListResource, '/v1_0/articles',
>                       endpoint='ArticleList')
> ```
>
> - 在`/toutiao/__init__.py`中已经注册了蓝图
>
>   ```python
>       ...
>       # 注册新闻模块蓝图
>       from .resources.news import news_bp
>       app.register_blueprint(news_bp)
>       ...
>   ```
>
>   

### 2.3 完成测试代码并运行测试

> 在`Test/test_f_rpc/test_rpc.py`中完成测试代码：
>
> ```python
> import requests, json
> 
> """测试 POST /v1_0/authorizations 登录请求"""
> # code参数：需要向主从redis中手动添加短信验证码用于测试
> # redis-cli -p 6380/6381
> # set app:code:13161933309 123456
> # 关于app:code:13161933309是一个redis key，该key的命名方式在
> # 在toutiao/resources/user/passport.py的SMSVerificationCodeResource类的get函数
> # redis 通过哨兵集群操作主从
> REDIS_SENTINELS = [('127.0.0.1', '26380'),
>                    ('127.0.0.1', '26381'),
>                    ('127.0.0.1', '26382'),]
> REDIS_SENTINEL_SERVICE_NAME = 'mymaster'
> from redis.sentinel import Sentinel
> _sentinel = Sentinel(REDIS_SENTINELS)
> redis_master = _sentinel.master_for(REDIS_SENTINEL_SERVICE_NAME)
> # redis_slave = _sentinel.slave_for(REDIS_SENTINEL_SERVICE_NAME)
> redis_master.set('app:code:18911111111', '123456')
> 
> """登录"""
> # 构造raw application/json形式的请求体
> data = json.dumps({'mobile': '18911111111', 'code': '123456'})
> # requests发送 POST raw application/json 登录请求
> url = 'http://192.168.45.128:5000/v1_0/authorizations'
> resp = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
> print(resp.json())
> 
> """测试 get /v1_0/articles"""
> # 从登录请求的响应中获取token
> token = resp.json()['data']['token']
> print(token)
> # 构造请求头：带着refresh_token发送请求
> headers = {'Authorization': 'Bearer {}'.format(token)}
> url = 'http://192.168.45.128:5000/v1_0/articles'
> args = {'channel_id': 1,}
> resp = requests.get(url, headers=headers, params=args)
> print(resp.json())
> ```
>
> - 启动`toutiao/main.py`并运行测试代码后发现抛出了异常
>
>   ```shell
>   	import reco_pb2 as reco__pb2
>   ImportError: attempted relative import with no known parent package
>   ```

### 2.3 解决导包异常

> 在/common/rpc/reco_pb2_grpc.py中，将
>
> > ```python
> > import reco_pb2 as reco__pb2
> > ```
>
> 修改为
>
> > ```python
> > try:
> >     import reco_pb2 as reco__pb2
> > except:
> >     from . import reco_pb2 as reco__pb2
> > ```
>
> 再测试运行，成功！

### 2.4 注意坑

> - 坑一
>
>   > flask.log日志显示如下
>   >
>   > ```shell
>   >   File "/home/python/toutiao-backend/toutiao/resources/news/article.py", line 16, in _get_rpc_article_list
>   >     user_request.user_id = user_id
>   > TypeError: 1162588537455902726 has type int, but expected one of: bytes, unicode
>   > ```
>   >
>   > **将异常中的`user_request.user_id = user_id`改为`user_request.user_id = str(user_id)`**
>
> - 坑二
>
>   > flask.log日志显示如下
>   >
>   > ```shell
>   >     raise _Rendezvous(state, None, None, deadline)
>   > grpc._channel._Rendezvous: <_Rendezvous of RPC that terminated with:
>   >         status = StatusCode.UNAVAILABLE
>   >         details = "Connect Failed"
>   > ```
>   >
>   > **请开启grpc服务进程，运行`common/rpc/server.py`**

## 3. 系统间使用grpc进行远程调用的注意事项

> rpc客户端和服务端双方都必须要有同一个proto文件生成的xxx_pb2.py和xxx_pb2_grpc.py两个文件
>
> 一旦约定调用的 类名、函数名、函数参数、函数返回数据结构 发生改变，那么双方就需要做相应的修改





