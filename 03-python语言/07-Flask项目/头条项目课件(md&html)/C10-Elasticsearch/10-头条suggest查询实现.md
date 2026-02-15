# 项目实现自动补全和纠错接口

[TOC]

<!-- toc -->

## 1. 需求

> 实现一个接口，对输入的关键词进行处理并返回
>
> - 先做自动补全，返回包含补全关键词的文章标题；
>
> - 如果没有补全的结果，就对关键词进行纠错，返回纠错后的关键词。

## 2. 思路

> - 先做自动补全，返回包含补全关键词的文章标题
>
>   > ```python
>   > # completions索引库！
>   > curl 127.0.0.1:9200/completions/words/_search?pretty -d '
>   > {
>   >     "from": 0,
>   >     "size": 10,
>   >     "_source": false,
>   >     "suggest": {
>   >         "word-completion" : {
>   >             "prefix" : "房价的看法即可登记反馈的减肥", 
>   >             "completion" : { 
>   >                 "field" : "suggest" 
>   >             }
>   >         }
>   >     }
>   > }
>   > '
>   > ```
>   >
>   > 终端返回结果
>   >
>   > ```shell
>   > ......
>   >  "suggest" : {
>   >     "word-completion" : [
>   >       {
>   >         "text" : "pyth",
>   >         "offset" : 0,
>   >         "length" : 4,
>   >         "options" : [
>   >           {
>   >             "text" : "Python 2 和 Python 3 主要区别有哪些（一）？",
>   > ......			
>   > # 要获取options = ret['suggest']['word-completion'][0]['options'] 判断是否为空[]
>   > ```
>
> - 如果没有补全的结果，就对关键词进行纠错，返回纠错后的关键词
>
>   > ```python
>   > curl 127.0.0.1:9200/articles/article/_search?pretty -d '
>   > {
>   >     "from": 0,
>   >     "size": 10,
>   >     "_source": false,
>   >     "suggest": {
>   >         "text": "pyhton",
>   >         "word-phrase": {
>   >             "phrase": {
>   >                 "field": "_all",
>   >                 "size": 1
>   >             }
>   >         }
>   >     }
>   > }
>   > '
>   > 
>   > ```
>   >
>   > 终端返回结果:
>   >
>   > ```shell
>   > ......
>   > "suggest" : {
>   >     "word-phrase" : [
>   >       {
>   >         "text" : "pyhton",
>   >         "offset" : 0,
>   >         "length" : 6,
>   >         "options" : [
>   >           {
>   >             "text" : "python",
>   >             ......
>   >             
>   > options = ret['suggest']['word-phrase'][0]['options'] 
>   > ```

## 3. 实现

### 3.1 注册路由

> 在`/resources/search/__init__.py`中注册视图
>
> ```python
> ......
> search_api.add_resource(search.SuggestionResource, '/v1_0/suggestion',
>                         endpoint='Suggestion')
> ```

### 3.2 完成视图

> 在`toutiao-backend/toutiao/resources/search.py`中实现自动补全+纠错视图
>
> ```python
> ......
> class SuggestionResource(Resource):
>     """文章搜索联想建议：不全就返回补全,如果没有结果就纠错"""
>     def get(self):
>         """1. 先尝试自动补全建议查询
>         2. 如果没得到查询结果，进行纠错建议查询"""
>         qs_parser = RequestParser()
>         qs_parser.add_argument('q', type=inputs.regex(r'^.{1,50}$'), required=True, location='args')
>         args = qs_parser.parse_args()
>         q = args.q
> 
>         # 先尝试自动补全建议查询
>         # http://192.168.45.128:5000/v1_0/suggestion?q=pyth
>         query = {
>             'from': 0,
>             'size': 10,
>             '_source': False,
>             'suggest': {
>                 'word-completion': { # word-completion自定义返回字段
>                     'prefix': q,
>                     'completion': {
>                         'field': 'suggest'
>                     }
>                 }
>             }
>         }
>         ret = current_app.es.search(index='completions', body=query)
>         options = ret['suggest']['word-completion'][0]['options']
> 
>         # 如果没得到查询结果，进行纠错建议查询
>         # http://192.168.45.128:5000/v1_0/suggestion?q=pythno
>         if not options:
>             query = {
>                 'from': 0,
>                 'size': 10,
>                 '_source': False,
>                 'suggest': {
>                     'text': q,
>                     'word-phrase': {
>                         'phrase': {
>                             'field': '_all',
>                             'size': 1
>                         }
>                     }
>                 }
>             }
>             ret = current_app.es.search(index='articles', doc_type='article', body=query)
>             options = ret['suggest']['word-phrase'][0]['options']
> 
>         results = []
>         for option in options:
>             if option['text'] not in results:
>                 results.append(option['text'])
> 
>         return {'options': results}
> 
> ```

## 4. 接口测试

> 测试代码
>
> ```python
> import requests
> url = 'http://192.168.45.128:5000/v1_0/suggestion?q=pythno'
> resp = requests.get(url)
> print(resp.json())
> 
> url = 'http://192.168.45.128:5000/v1_0/suggestion?q=pyth'
> resp = requests.get(url)
> print(resp.json())
> ```