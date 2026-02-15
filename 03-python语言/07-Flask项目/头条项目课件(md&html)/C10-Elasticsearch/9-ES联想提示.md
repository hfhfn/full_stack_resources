# ES拼写纠错和自动补全

> ES具有拼写纠错和自动补全功能，称为suggest建议查询模式；其中自动补全需要单独建立专门的索引库

[TOC]

<!-- toc -->

## 1. 拼写纠错

> - 对于已经建立的articles索引库，elasticsearch还提供了一种查询模式，suggest建议查询模式
>
>   > ```shell
>   > # word-phrase 自定义字段名, 推荐结果会包含在该字段中
>   > # phrase 按短语、词组搜索 进行纠错
>   > # field 指定在哪些字段中获取推荐词
>   > # size 返回的推荐词数量
>   > curl 127.0.0.1:9200/articles/article/_search?pretty -d '
>   > {
>   >  "from": 0,
>   >  "size": 10,
>   >  "_source": false,
>   >  "suggest": {
>   >      "text": "phtyon",
>   >      "word-phrase": {
>   >          "phrase": {
>   >              "field": "_all",
>   >              "size": 1
>   >          }
>   >      }
>   >  }
>   > }'
>   > ```
>   >
>   > 
>
> - 当我们输入错误的关键词`phtyon web`时，es可以提供根据索引库数据得出的正确拼写`python web`
>
>   > ```shell
>   > ......
>   > "suggest" : {
>   >  "word-phrase" : [
>   >    {
>   >      "text" : "phtyon web", # 输入的结果
>   >      "offset" : 0,
>   >      "length" : 10,
>   >      "options" : [
>   >        {
>   >          "text" : "python web", # 拼写纠错结果
>   >          "score" : 7.591972E-4
>   >        }
>   >      ]
>   >    }
>   >  ]
>   > }
>   > }
>   > ```
>   >
>   > 

## 2. 自动补全

> 当前有一个需求是：根据输入要返回自动补全的文章title；那我们就可以利用es的自动补全索引来实现

### 2.1 新建自动补全的索引库

> **如果要使用elasticsearch提供的自动补全功能**，因为文档的类型映射要特殊设置，所以原先建立的文章索引库不能用于自动补全，**需要再建立一个自动补全的索引库**
>
> - 创建索引
>
>   > ```shell
>   > curl -X PUT 127.0.0.1:9200/completions -H 'Content-Type: application/json' -d'
>   > {
>   > "settings" : {
>   >     "index": {
>   >         "number_of_shards" : 3,
>   >         "number_of_replicas" : 1
>   >     }
>   > }
>   > }
>   > '
>   > ```
>   >
>   > 
>
> - 创建类型映射
>
>   > ```shell
>   > # "type": "completion", 自动补全的类型必须completion
>   > curl -X PUT 127.0.0.1:9200/completions/_mapping/words -H 'Content-Type: application/json' -d'
>   > {
>   >   "words": {
>   >        "properties": {
>   >            "suggest": {
>   >                "type": "completion",
>   >                "analyzer": "ik_max_word"
>   >            }
>   >        }
>   >   }
>   > }
>   > '
>   > ```
>   >
>   > 

### 2.2 使用logstash导入初始数据

#### 2.2.1 新建`logstash_mysql_completion.conf`只把`title`导入索引

> ```shell
> input{
>      jdbc {
>          jdbc_driver_library => "/home/python/mysql-connector-java-8.0.13/mysql-connector-java-8.0.13.jar"
>          jdbc_driver_class => "com.mysql.jdbc.Driver"
>          jdbc_connection_string => "jdbc:mysql://127.0.0.1:3306/toutiao?tinyInt1isBit=false"
>          jdbc_user => "root"
>          jdbc_password => "mysql"
>          jdbc_paging_enabled => "true"
>          jdbc_page_size => "1000"
>          jdbc_default_timezone =>"Asia/Shanghai"
>          statement => "select title as suggest from news_article_basic" 
>          clean_run => true
>      }
> }
> output{
>       elasticsearch {
>          hosts => "127.0.0.1:9200"
>          index => "completions"
>          document_type => "words"
>       }
> }
> ```

#### 2.2.2 执行命令导入数据

> ```shell
> sudo /usr/share/logstash/bin/logstash -f ./logstash_mysql_completion.conf
> ```

### 2.3 自动补全建议查询

> ```shell
> # 自动补全对类型映射有特殊要求, 不能使用原索引库, 需要创建单独的自动补全索引库，看上边
> # title-suggest 自定义字段名, 推荐结果会包含在该字段中
> # prefix 要补全的关键词
> # completion 映射的类型，在建立自动补全索引时，声明的type的类型，固定值
> # field 指定在哪些字段中获取推荐词
> curl 127.0.0.1:9200/completions/words/_search?pretty -d '
> {
>     "suggest": {
>         "title-suggest" : {
>             "prefix" : "pyth", 
>             "completion" : { 
>                 "field" : "suggest" 
>             }
>         }
>     }
> }
> '
> 
> # 对词组进行自动补全查询
> curl 127.0.0.1:9200/completions/words/_search?pretty -d '
> {
>     "suggest": {
>         "title-suggest" : {
>             "prefix" : "python web", 
>             "completion" : { 
>                 "field" : "suggest" 
>             }
>         }
>     }
> }
> '
> ```
>
> - 自动补全对类型映射有特殊要求, 不能使用原索引库, 需要创建`单独的自动补全索引库`
> - 注意   推荐词的映射类型必须是`completion`