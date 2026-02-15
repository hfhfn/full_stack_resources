# 文档的查询

[TOC]

<!-- toc -->

## 1. 基本查询

> 使用查询字符串来查询
>
> - url最后如果有查询字符串那么多参数就必须多加一个 `\`，比如`?_source=title,user_id\&pretty`
> - 如果查询字符串中一个key有多个值，就用逗号`,`隔开

### 1.1 根据文档ID

> ```shell
> curl -X GET 127.0.0.1:9200/articles/article/1
> curl -X GET 127.0.0.1:9200/articles/article/1?_source=title,user_id\&pretty
> curl -X GET 127.0.0.1:9200/articles/article/1?_source=false\&pretty # 不显示数据
> ```

### 1.2 查询所有数据

> ```shell
> curl -X GET 127.0.0.1:9200/articles/article/_search?_source=title,user_id\&pretty
> ```
>
> 查询结果如下，最多展示10条
>
> ```bash
> {                                                                                     "took" : 5, #5毫秒                                                                     "timed_out" : false, #没有超时
>   "_shards" : {
>     "total" : 3, # 三个主分片获取来的数据
>     "successful" : 3,
>     "skipped" : 0,
>     "failed" : 0
>   },
>   "hits" : {
>     "total" : 2017, # 文档总数
>     "max_score" : 1.0, # 本次搜索的search的最大相关性得分，此处的1.0没有意义
>     "hits" : [{},{},... # 数据
> ```

### 1.3 分页

> - from 起始
> - size 每页数量
>
> ```shell
> curl -X GET 127.0.0.1:9200/articles/article/_search?_source=title,user_id\&size=3\&pretty
> 
> curl -X GET 127.0.0.1:9200/articles/article/_search?_source=title,user_id\&size=3\&from=10\&pretty
> ```

### 1.4 全文检索

> ```shell
> # 从content字段中查询 'python web'
> curl -X GET 127.0.0.1:9200/articles/article/_search?q=content:python%20web\&_source=title,article_id\&pretty
> # 从content和title字段中同时查询 'python web'
> curl -X GET 127.0.0.1:9200/articles/article/_search?q=title:python%20web,content:python%20web\&_source=title,article_id\&pretty
> # 从所有字段中查询 'python web'，按文档中有最高匹配度字段来计算匹配得分
> curl -X GET 127.0.0.1:9200/articles/article/_search?q=_all:python%20web\&_source=title,article_id\&pretty
> ```
>
> - `%20` 表示空格



## 2. 高级查询

> 使用请求体来进行查询

### 2.1 全文检索`match`

> ```shell
> # 对python web进行分词后检索
> curl -X GET 127.0.0.1:9200/articles/article/_search?pretty -d'
> {
>  "query" : {
>      "match" : {
>          "title" : "python web"
>      }
>  }
> }'
> # _source 规定返回结果
> curl -X GET 127.0.0.1:9200/articles/article/_search?pretty -d'
> {
>  "from": 0,
>  "size": 5,
>  "_source": ["article_id","title"],
>  "query" : {
>      "match" : {
>          "title" : "python web"
>      }
>  }
> }'
> 
> curl -X GET 127.0.0.1:9200/articles/article/_search?pretty -d'
> {
>  "from": 0,
>  "size": 5,
>  "_source": ["article_id","title"],
>  "query" : {
>      "match" : {
>          "_all" : "python web 编程"
>      }
>  }
> }'
> ```

### 2.2 短语搜索`match_phrase`

> ```shell
> # match_phrase 不做分词
> # _all 对每一个字段都进行查询，只要有一个字段相似就算
> curl -X GET 127.0.0.1:9200/articles/article/_search?pretty -d'
> {
>  "size": 5,
>  "_source": ["article_id","title"],
>  "query" : {
>      "match_phrase" : {
>          "_all" : "python web"
>      }
>  }
> }'
> ```

### 2.3 精确查找`term `

> ```shell
> # 查询条件user_id=1 不会分词, 必须能够匹配到词条(索引库中必须有该词条)
> curl -X GET 127.0.0.1:9200/articles/article/_search?pretty -d'
> {
>  "size": 5,
>  "_source": ["article_id","title", "user_id"],
>  "query" : {
>      "term" : {
>          "user_id" : 1
>      }
>  }
> }'
> ```

### 2.4 范围查找`range`

> ```shell
> # gte大于等于 gt大于 lte小于等于 lt小于
> curl -X GET 127.0.0.1:9200/articles/article/_search?pretty -d'
> {
>  "size": 5,
>  "_source": ["article_id","title", "user_id"],
>  "query" : {
>      "range" : {
>          "article_id": { 
>              "gte": 3,
>              "lte": 5
>          }
>      }
>  }
> }'
> ```

### 2.5 高亮搜索`highlight`

> ```shell
> curl -X GET 127.0.0.1:9200/articles/article/_search?pretty -d '
> {
>     "size":2,
>     "_source": ["article_id", "title", "user_id"],
>     "query": {
>         "match": {
>              "title": "python web 编程"
>          }
>      },
>      "highlight":{
>           "fields": {
>               "title": {}
>           }
>      }
> }
> '
> ```

### 2.6 组合查询

> ```shell
> curl -X GET 127.0.0.1:9200/articles/article/_search?pretty -d '
> {
>  "_source": ["title", "user_id"],
>  "query": {
>      "bool": {
>          "must": {
>              "match": {
>                  "title": "python web"
>              }
>          },
>          "filter": {
>              "term": {
>                  "user_id": 2
>              }
>          }
>      }
>  }
> }
> '
> ```
>
> - must
>
> 文档 必须 匹配这些条件才能被查询
>
> - must_not
>
> 文档 必须不 匹配这些条件才能被查询
>
> - should
>
> 如果某条文档符合should规定的查询条件，那么一定会被查询，而且匹配度得分会被提高
>
> - filter
>
> 对结果再进行过滤，不影响匹配度评分。

### 2.7 排序

> ```shell
> curl -X GET 127.0.0.1:9200/articles/article/_search?pretty -d'
> {
>     "size": 5,
>     "_source": ["article_id","title"],
>     "query" : {
>         "match" : {
>             "_all" : "python web"
>         }
>     },
>     "sort": [
>         { "create_time":  { "order": "desc" }},
>         { "_score": { "order": "desc" }}
>     ]
> }'
> ```

### 2.8 `boost`提升权重优化排序

> ```shell
> # 被查询的文档的得分乘以4
> curl -X GET 127.0.0.1:9200/articles/article/_search?pretty -d'
> {
>  "size": 5,
>  "_source": ["article_id","title"],
>  "query" : {
>      "match" : {
>          "title" : {
>              "query": "python web",
>              "boost": 4
>          }
>      }
>  }
> }'
> ```