# 完成rpc服务端代码

[TOC]

<!-- toc -->

## 1. gRPC使用流程

> - 根据proto3协议对应的`接口定义语言`来描述接口需求
>   - 用proto3语法写一个proto文件
> - 使用gRPC的编译器生成对应平台的客户端和服务端代码
>   - 用命令行生成python代码
> - 实现客户端和服务端的具体逻辑
>   - **服务端的代码  → 这是本章节要完成的步骤**
>   - 完成客户端的代码

## 2. 完成rpc服务端的代码

> > 为了学习gRPC，并为了看到rpc的效果，我们编写补全服务端代码。
> >
> > **注意：此处实际的代码应该运行在推荐系统中，而不是运行在web系统中**，因为是web系统要调用推荐系统的RPC服务
>
> 在toutiao-backend/common/rpc目录下新建server.py文件，按步骤完成rpc服务端的模拟代码

### 2.1 完成rpc服务端被调用函数的代码

> 在`toutiao-backend/common/rpc/server.py中`
>
> ```python
> import time
> # todo 这里模拟rpc服务端处理数据
> 
> """gRPC 被调用的类和方法（写在服务端）"""
> import reco_pb2
> import reco_pb2_grpc
> 
> class UserRecommendService(reco_pb2_grpc.UserRecommendServicer):
>  # 继承父类 ‘reco_pb2_grpc.proto文件中声明类名Servicer’
>  def user_recommend(self, request, context):
>      """重写同名函数，对应proto文件中声明的函数名
>      # step 1. 解析接收的请求参数
>      # step 2. 处理并返回响应数据
>      :param request: 调用时的请求参数对象
>      :param context: 用来设置调用返回的异常信息
>      :return: response = reco_pb2.ArticleResponse() 实例化的rpc服务函数返回的响应对象
>      """
>      # 解析接收的请求参数
>      # 在proto文件中声明是什么类型的，那么解析出来的参数也就是相应的类型
>      user_id = request.user_id
>      channel_id = request.channel_id
>      article_num = request.article_num
>      time_stamp = request.time_stamp
>      print('接收到了rpc请求的参数')
> 
>      # 处理并返回 实例化的rpc服务函数返回的响应对象
>      # reco_pb2.ArticleResponse() 中的 ArticleResponse 就是proto文件中声明的响应对象的名字
>      response = reco_pb2.ArticleResponse()
>      """这里是模拟构造的 返回的数据！ 每个属性名和proto文件中声明都一一对应"""
>      response.expousre = '曝光埋点数据'
>      # 一般时间戳都是以毫秒为单位，py以秒为单位 round四舍五入转为整型
>      response.time_stamp = round(time.time() * 1000)
> 
>      recommends = [] # python list 对应proto中repeated类型
>      for i in range(article_num): # 模拟构造具体推荐文章的信息，数量就是请求参数中携带的 article_num
>          article = reco_pb2.Article() # reco_pb2.Article()对应roto文件中声明的 message Article
>          article.article_id = i+1
>          # 对于响应对象中的嵌套结构，已经在自动生成的reco_pb2.py文件中实现过了
>          # 所以这里不用写了！！！
>          # article.track = reco_pb2.Track() # reco_pb2.Track() 对应roto文件中声明的 message Track
>          article.track.click = '用户点击行为的埋点参数'
>          article.track.collect = '用户收藏的埋点参数'
>          article.track.share = '用户分享的埋点参数'
>          article.track.read = '用户进入文章详情的埋点参数'
>          recommends.append(article) # 把每个推荐文章的约定返回参数添加到python list中
>      # 对于列表类型的赋值，必须使用response.约定的repeated类型名.extend(python_list)
>      response.recommends.extend(recommends)
> 
>      return response # 返回
> ```
>
> - 思考：代码中为什么声明`article = reco_pb2.Article()` 而不声明 `article.track = reco_pb2.Track()` 呢？
>   - Article是recommends（list）中的元素对象，有多个
>   - proto中repeated类型中的嵌套元素，必须要声明！

### 2.2 完成rpc服务端server的代码

> 在`toutiao-backend/common/rpc/server.py中`
>
> ```python
> ......
> """gRPC server"""
> import grpc # pip install grpcio 安装名和导包名不一样！
> # concurrent是python32开始自带包：并发工具箱 # https://www.cnblogs.com/JerryZao/p/9873824.html
> from concurrent.futures import ThreadPoolExecutor
> 
> 
> def serve():
>     """rpc服务启动函数
>     # 1. 创建一个rpc服务器
>     # 1.1 指定使用线程池处理器 concurrent.futures.ThreadPoolExecutor
>     # 2. 向服务器中添加被调用的服务方法
>     # 3. rpc服务绑定ip地址和端口
>     # 4. 启动rpc服务，不会阻塞程序
>     # 5. 不断循环防止程序退出
>     """
>     # 1. 创建一个rpc服务器
>     # 指定使用concurrent.futures.ThreadPoolExecutor线程池处理器，并规定池大小有3个线程
>     server = grpc.server(ThreadPoolExecutor(max_workers=3))
>     # 2. 向服务器中添加被调用的服务方法
>     # reco_pb2_grpc.add_约定的类名Servicer_to_server(继承并重新的处理数据的子类(), grpc_server对象)
>     reco_pb2_grpc.add_UserRecommendServicer_to_server(UserRecommendServicer(), server)
>     # 3. rpc服务绑定ip地址和端口
>     server.add_insecure_port('0.0.0.0:8888')
>     # 4. 启动rpc服务，不会阻塞程序
>     server.start()
>     # 5. 不断循环防止程序退出
>     while True: time.sleep(100)
> 
> 
> if __name__ == '__main__':
> 
>     serve()
> ```

## 3. 完整参考代码

> 在`toutiao-backend/common/rpc/server.py`中
>
> ```python
> import time
> # todo 这里模拟rpc服务端处理数据
> 
> """gRPC 被调用的类和方法（写在服务端）"""
> import reco_pb2
> import reco_pb2_grpc
> 
> class UserRecommendServicer(reco_pb2_grpc.UserRecommendServicer):
>  # 继承父类 ‘reco_pb2_grpc.proto文件中声明类名Servicer’
>  def user_recommend(self, request, context):
>      """重写同名函数，对应proto文件中声明的函数名
>      # step 1. 解析接收的请求参数
>      # step 2. 处理并返回响应数据
>      :param request: 调用时的请求参数对象
>      :param context: 用来设置调用返回的异常信息
>      :return: response = reco_pb2.ArticleResponse() 实例化的rpc服务函数返回的响应对象
>      """
>      # 解析接收的请求参数
>      # 在proto文件中声明是什么类型的，那么解析出来的参数也就是相应的类型
>      user_id = request.user_id
>      channel_id = request.channel_id
>      article_num = request.article_num
>      time_stamp = request.time_stamp
>      print('接收到了rpc请求的参数')
> 
>      # 处理并返回 实例化的rpc服务函数返回的响应对象
>      # reco_pb2.ArticleResponse() 中的 ArticleResponse 就是proto文件中声明的响应对象的名字
>      response = reco_pb2.ArticleResponse()
>      """这里是模拟构造的 返回的数据！ 每个属性名和proto文件中声明都一一对应"""
>      response.expousre = '曝光埋点数据'
>      # 一般时间戳都是以毫秒为单位，py以秒为单位 round四舍五入转为整型
>      response.time_stamp = round(time.time() * 1000)
> 
>      recommends = [] # python list 对应proto中repeated类型
>      for i in range(article_num): # 模拟构造具体推荐文章的信息，数量就是请求参数中携带的 article_num
>          article = reco_pb2.Article() # reco_pb2.Article()对应roto文件中声明的 message Article
>          article.article_id = i+1
>          # 对于响应对象中的嵌套结构，已经在自动生成的reco_pb2.py文件中实现过了
>          # article和recommends没有直接的嵌套关系（recommends:[{article1}, {article2}]）
>          # track和article有直接的嵌套关系（类似dict），所以不需要额外声明！
>          # 所以这里不用写了！！！
>          # X! article.track = reco_pb2.Track() # reco_pb2.Track() 对应roto文件中声明的 message Track
>          article.track.click = '用户点击行为的埋点参数'
>          article.track.collect = '用户收藏的埋点参数'
>          article.track.share = '用户分享的埋点参数'
>          article.track.read = '用户进入文章详情的埋点参数'
>          recommends.append(article) # 把每个推荐文章的约定返回参数添加到python list中
>      # 对于列表类型的赋值，必须使用response.约定的repeated类型名.extend(python_list)
>      response.recommends.extend(recommends)
> 
>      return response # 返回
> 
> 
> """gRPC server"""
> import grpc # pip install grpcio 安装名和导包名不一样！
> # concurrent是python32开始自带包：并发工具箱 # https://www.cnblogs.com/JerryZao/p/9873824.html
> from concurrent.futures import ThreadPoolExecutor
> import reco_pb2_grpc
> 
> 
> def serve():
>  """rpc服务启动函数
>  # 1. 创建一个rpc服务器
>  # 1.1 指定使用线程池处理器 concurrent.futures.ThreadPoolExecutor
>  # 2. 向服务器中添加被调用的服务方法
>  # 3. rpc服务绑定ip地址和端口
>  # 4. 启动rpc服务，不会阻塞程序
>  # 5. 不断循环防止程序退出
>  """
>  # 1. 创建一个rpc服务器
>  # 指定使用concurrent.futures.ThreadPoolExecutor线程池处理器，并规定池大小有3个线程
>  server = grpc.server(ThreadPoolExecutor(max_workers=3))
>  # 2. 向服务器中添加被调用的服务方法
>  # reco_pb2_grpc.add_约定的类名Servicer_to_server(继承并重新的处理数据的子类(), grpc_server对象)
>  reco_pb2_grpc.add_UserRecommendServicer_to_server(UserRecommendServicer(), server)
>  # 3. rpc服务绑定ip地址和端口
>  server.add_insecure_port('0.0.0.0:8888')
>  # 4. 启动rpc服务，不会阻塞程序
>  server.start()
>  # 5. 不断循环防止程序退出
>  while True: time.sleep(100)
> 
> 
> if __name__ == '__main__':
> 
>  serve()
> ```

