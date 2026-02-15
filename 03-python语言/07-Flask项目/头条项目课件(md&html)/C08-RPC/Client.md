# 完成rpc客户端代码

[TOC]

<!-- toc -->

## 1. gRPC使用流程

> - 根据proto3协议对应的`接口定义语言`来描述接口需求
>   - 用proto3语法写一个proto文件
> - 使用gRPC的编译器生成对应平台的客户端和服务端代码
>   - 用命令行生成python代码
> - 实现客户端和服务端的具体逻辑
>   - 服务端的代码
>   - **完成客户端的代码  → 这是本章节要完成的步骤**

## 2. 完成rpc客户端代码

> 在`toutiao-backend/common/rpc`目录下新建`client.py`

### 2.1 完成调用执行grpc远程函数并获取结果的方法

> ```python
> import time
> import reco_pb2
> 
> 
> """完成调用执行grpc远程函数 并获取结果的方法"""
> def get_grpc_func_ret(stub):
>     # 构建rpc调用的调用参数
>     user_request = reco_pb2.UserRequest() # 实例化请求参数对象 对应proto文件中的UserRequest
>     user_request.user_id = '1'
>     user_request.channel_id = 1
>     user_request.article_num = 10
>     user_request.time_stamp = round(time.time()*1000)
> 
>     # 通过stub进行方法调用，并接收调用返回值
>     rpc_ret = stub.user_recommend(user_request) # 对应proto文件中的user_recommend函数
>     print(rpc_ret)
>     print(rpc_ret.recommends[0].track.click)
>     return rpc_ret
> ```

### 2.2 完成grpc客户端执行的代码

> ```python
> import grpc
> import reco_pb2_grpc
> ......
> """完成grpc客户端执行的代码"""
> def run():
>     """rpc客户端运行的方法"""
>     	# 使用with语句连接rpc服务器
>        with grpc.insecure_channel('127.0.0.1:8888') as channel:
>            # 创建调用rpc远端服务的辅助对象stub
>            stub = reco_pb2_grpc.UserRecommendStub(channel)
>            # 通过stub进行rpc调用
>            return get_grpc_func_ret(stub)
> 
> if __name__ == '__main__':
>     	run()
> ```

## 3. 完整参考代码

> ```python
> import time
> import reco_pb2
> import grpc
> import reco_pb2_grpc
> 
> 
> """完成调用执行grpc远程函数 并获取结果的方法"""
> def get_grpc_func_ret(stub):
>     # 构建rpc调用的调用参数
>     user_request = reco_pb2.UserRequest() # 实例化请求参数对象 对应proto文件中的UserRequest
>     user_request.user_id = '1'
>     user_request.channel_id = 1
>     user_request.article_num = 10
>     user_request.time_stamp = round(time.time()*1000)
> 
>     # 通过stub进行方法调用，并接收调用返回值
>     rpc_ret = stub.user_recommend(user_request) # 对应proto文件中的user_recommend函数
>     print(rpc_ret)
>     print(rpc_ret.recommends[0].track.click)
>     return rpc_ret
> 
> 
> """完成grpc客户端执行的代码"""
> def run():
>     """rpc客户端运行的方法"""
>     # 使用with语句连接rpc服务器
>     with grpc.insecure_channel('127.0.0.1:8888') as channel:
>         # 创建调用rpc远端服务的辅助对象stub
>         stub = reco_pb2_grpc.UserRecommendStub(channel)
>         # 通过stub进行rpc调用
>         return get_grpc_func_ret(stub)
> 
> 
> if __name__ == '__main__':
>     run()
> ```