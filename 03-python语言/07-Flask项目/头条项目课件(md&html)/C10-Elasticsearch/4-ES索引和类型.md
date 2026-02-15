# Elasticsearch索引和类型

[TOC]

<!-- toc -->

## 1. 索引的相关操作

### 1.1 创建索引(数据库)

> - 创建名为articles的索引
>   - `"number_of_shards" : 3,`主分片数
>   - `"number_of_replicas" : 1`  从库数量
>
> ```shell
> # PUT /articles 创建名为articles的索引
> curl -X PUT 127.0.0.1:9200/articles -H 'Content-Type: application/json' -d'
> {
>        "settings" : {
>             "index": {
>                 "number_of_shards" : 3,
>                 "number_of_replicas" : 1
>                }
>        }
> }
> '
> ```

### 1.2 查看所有索引库

> ```shell
>  curl 127.0.0.1:9200/_cat/indices
> ```

### 1.3 删除索引库

> ```shell
> curl -X DELETE 127.0.0.1:9200/articles # 删除articles索引库
> ```

## 2. 类型和映射

### 2.1 概念

> - 类型, 相当于数据库的表
> - 设置类型映射, 相当于描述表结构(字段名称, 字段类型)并建表

### 2.2 字段的类型

> - 字符串: `text` (在elaticsearch 2.x版本中，为string类型)
>
> - 整数 : `byte`, `short`, `integer`, `long`
> - 浮点数: `float`, `double`
> - 布尔型: `boolean`
> - 日期: `date`

### 2.3 创建头条项目的文章类型映射

> ```shell
> # PUT /articles/_mapping/article 对articles索引创建名为article的类型映射
> curl -X PUT 127.0.0.1:9200/articles/_mapping/article -H 'Content-Type: application/json' -d'
> {
>      "_all": {
>           "analyzer": "ik_max_word"
>       },
>       "properties": {
>           "article_id": {
>               "type": "long",
>               "include_in_all": "false"
>           },
>           "user_id": {
>               "type": "long",
>               "include_in_all": "false"
>           },
>           "title": {
>               "type": "text",
>               "analyzer": "ik_max_word",
>               "include_in_all": "true",
>               "boost": 2
>           },
>           "content": {
>               "type": "text",
>               "analyzer": "ik_max_word",
>               "include_in_all": "true"
>           },
>           "status": {
>               "type": "integer",
>               "include_in_all": "false"
>           },
>           "create_time": {
>               "type": "date",
>               "include_in_all": "false"
>           }
>       }
> }
> '
> ```
>
> - 解读
>
>   > - `_mapping` 设置类型映射的接口 
>   > - `/article`  类型, 对应一张表
>   > - properties  指定字段名称和类型  
>   >   - `以查询为目的`建立字段
>   >   - `标题/内容 `为用户提供`查询使用的字段`
>   >   - 文章id/作者id/文章状态/发布时间  主要给`后台管理`查询使用
>   >   - _all字段默认会包含所有字段的关键词, 比如查询关键词时, 不设置查询条件, 既查询标题也查询内容, 则可以使用__all字段查询
>   >   - include_in_all则是设置该字段的关键词是否加入到_all字段的关键词中，false表示不用
>   >     - user_id, article_id不加入_all, 这样用户查询时, 可以直接查询__all字段
>   >     - 后台查询,可以根据需求进行查询
>   >   - analyzer 分析器设置, 只对字符串类型(text)有效 
>   >   - boost 设置相关性排序的权重  整数形式, 尽量控制在10以内

### 2.4 查看映射

> ```shell
> curl 127.0.0.1:9200/articles?pretty  # 查询articles的整个索引库结构
> curl 127.0.0.1:9200/articles/_mapping/article?pretty  # 查询article表的结构
> # 不设置-X默认为GET
> ```

### 2.5 修改索引库的类型映射

> - 可以增加字段，但不能修改已有字段的类型(索引的建立和类型有关)
>   - 只能建立新的库, 重新进行类型映射
>   - 好处是**不需要将数据再导入到新的索引库, 只需要重新索引数据**
>
> ```shell
> # 5.x版本需要分别设置配置和类型映射
> # PUT /articles_v2 创建新的索引库articles_v2 
> curl -X PUT 127.0.0.1:9200/articles_v2 -H 'Content-Type: application/json' -d'
> {
>    "settings" : {
>       "index": {
>           "number_of_shards" : 3,
>           "number_of_replicas" : 1
>        }
>    }
> }
> '
> # PUT /articles_v2/_mapping/article 对articles_v2索引创建名为article的类型映射
> curl -X PUT 127.0.0.1:9200/articles_v2/_mapping/article -H 'Content-Type: application/json' -d'
> {
>      "_all": {
>           "analyzer": "ik_max_word"
>       },
>       "properties": {
>           "article_id": {
>               "type": "long",
>               "include_in_all": "false"
>           },
>           "user_id": {
>                "type": "long",
>               "include_in_all": "false"
>           },
>           "title": {
>               "type": "text",
>               "analyzer": "ik_max_word",
>               "include_in_all": "true",
>               "boost": 2
>           },
>           "content": {
>               "type": "text",
>               "analyzer": "ik_max_word",
>               "include_in_all": "true"
>           },
>           "status": {
>               "type": "byte",
>               "include_in_all": "false"
>           },
>           "create_time": {
>               "type": "date",
>               "include_in_all": "false"
>           }
>       }
> }'
> 
> # POST /_reindex 重新索引数据，把articles的数据索引到articles_v2
> curl -X POST 127.0.0.1:9200/_reindex -H 'Content-Type:application/json' -d '
> {
>   "source": {
>     "index": "articles"
>   },
>   "dest": {
>     "index": "articles_v2"
>   }
> }
> '
> ```

### 2.6 删除索引

> ```shell
> curl -X DELETE 127.0.0.1:9200/articles  # 删除articles1索引库
> ```

### 2.7 给索引起别名

> 如果修改索引库, 代码中的库名称也要对应修改, 为了避免代码的改动, 可以给新的索引库起别名, 让其使用原库的名称
>
> ```shell
> curl -X DELETE 127.0.0.1:9200/articles  # 先删除原索引库
> curl -X PUT 127.0.0.1:9200/articles_v2/_alias/articles  # 给索引库起别名, 设置为原索引库的名称
> ```
>
> - 注意先删除原库, 避免出现名称冲突

### 2.8 查询索引别名

> ```shell
> # 查看别名指向哪个索引
> curl 127.0.0.1:9200/*/_alias/articles
> 
> # 查看哪些别名指向这个索引
> curl 127.0.0.1:9200/articles_v2/_alias/*
> ```

## 3. 查看集群健康状态

> ```powershell
> curl GET 127.0.0.1:9200/_cluster/health?pretty
> # 集群做健康状态检查会耗费一些时间
> 
> {
> "cluster_name" : "elasticsearch", # 集群主节点名称
> "status" : "yellow", # 集群健康状态
> "timed_out" : false, # 是否超时
> "number_of_nodes" : 1, # 集群节点数
> "number_of_data_nodes" : 1, # 数据节点数
> "active_primary_shards" : 3, # 活跃的主分片数
> "active_shards" : 3, # 活跃的分片数
> "relocating_shards" : 0, # 当前节点迁往其他节点的分片数量，通常为0，当有节点加入或者退出时该值会增加
> "initializing_shards" : 0, # 正在初始化的分片
> "unassigned_shards" : 3, # 未分配的分片数，通常为0，当有某个节点的副本分片丢失该值就会增加，此时3个副本分片没有用起来，没有进行分配使用
> "delayed_unassigned_shards" : 0, # 延迟的未分配的分片数
> "number_of_pending_tasks" : 0, # 是指主节点创建索引并分配shards等任务的数量，如果该指标数值一直未减小代表集群存在不稳定因素，pending task只能由主节点来进行处理，这些任务包括创建索引并将shards分配给节点
> "task_max_waiting_in_queue_millis" : 0, # 任务在等待执行时最大等待时长
> "active_shards_percent_as_number" : 50.0 # 集群分片健康度，活跃分片数占总分片数比例。
> }
> ```
>
> - `status` 字段指示着当前集群在总体上是否工作正常。它的三种颜色含义如下：
>
>   > - `green`
> >
>   >   所有的主分片和副本分片都正常运行。
> >
>   > - `yellow`
> >
>   >   预警状态，所有主分片功能正常，但至少有一个副本是不能正常工作的。此时集群是可以正常工作的，没有数据丢失，因此搜索结果仍将完整。
> >
>   > - `red`
> >
>   >     有主分片没能正常运行。
>   
> - **本例中的健康状态为yellow的原因是因为单点单节点部署Elasticsearch**
>
>   > 单点部署Elasticsearch, 默认的分片副本数目配置为1，而相同的分片不能在一个节点上，所以就存在副本分片指定不明确的问题，所以显示为yellow，可以通过在Elasticsearch集群上添加一个节点来解决问题，如果不想这么做，可以删除那些指定不明确的副本分片（当然这不是一个好办法）但是作为测试和解决办法还是可以尝试的，下面是删除副本分片的办法:
>   >
>   > ```shell
>   > curl -XPUT 127.0.0.1:9200/_settings -d '{"number_of_replicas": 0}'
>   > # 本例中你无需这么做！
>   > ```

## 4. 课后拓展阅读

> - [es集群健康状态](https://blog.csdn.net/laoyang360/article/details/81271491)
> - [更加深入的了解es集群1](http://www.sohu.com/a/336106807_315839)
> - [更加深入的了解es集群2](https://www.cnblogs.com/kevingrace/p/10671063.html)
> - [ES权威指南中文版](https://es.xiaoleilu.com/)



