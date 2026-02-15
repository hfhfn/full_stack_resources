# 文档的增删改

> 在Elasticsearch中，一条数据就是文档

[TOC]

<!-- toc -->

## 1. 一个文档的实例

> ```json
> {
>     "name":         "John Smith",
>     "age":          42,
>     "confirmed":    true,
>     "join_date":    "2014-06-01",
>     "home": {
>         "lat":      51.5,
>         "lon":      0.1
>     },
>     "accounts": [
>         {
>             "type": "facebook",
>             "id":   "johnsmith"
>         },
>         {
>             "type": "twitter",
>             "id":   "johnsmith"
>         }
>     ]
> }
> ```
>
> 一个文档不仅仅包含它的数据 ，也包含 *元数据*(metadata) —— 有关文档的信息。 三个必须的元数据元素如下：
>
> - `_index`
>
>   文档在哪存放
>
> - `_type`
>
>   文档表示的对象类别
>
> - `_id`
>
>   文档唯一标识

## 2. 索引文档(保存文档数据)

> - 使用自定义的文档id
>
> ```http
> PUT /{index}/{type}/{id}
> {
>   "field": "value",
>   ...
> }
> ```
>
> - 自动生成文档id
>
> ```http
> PUT /{index}/{type}
> {
>   "field": "value",
>   ...
> }
> ```
>
> - 试一试
>
> ```json
> curl -X PUT 127.0.0.1:9200/articles/article/150000 -H 'Content-Type:application/json' -d '
> {
>   "article_id": 150000,
>   "user_id": 1,
>   "title": "python是世界上最好的语言",
>   "content": "确实如此",
>   "status": 2,
>   "create_time": "2019-04-03"
> }'
> ```

## 3. 获取指定文档

> ```shell
> curl 127.0.0.1:9200/articles/article/150000?pretty
> 
> # 获取一部分
> curl 127.0.0.1:9200/articles/article/150000?_source=title,content\&pretty
> ```
>
> 注意：`_version` 每次修改文档数据，版本都会增加，可以当作乐观锁的依赖（判断标准）使用

## 4. 判断文档是否存在

> ```shell
> curl -i -X HEAD 127.0.0.1:9200/articles/article/150000
> ```
>
> - 存在 200状态码
> - 不存在 404状态码
> - ctrl+C退出 

## 5. 更新文档

> 在 Elasticsearch 中文档是 不可改变的，不能修改它们。 相反，如果想要更新现有的文档，需要重建索引或者进行替换。我们可以使用相同的 `index` API 进行实现。
>
> - 不能更新，只能重存，`_version`会变化
>
> - 例如修改title字段的内容，不可进行以下操作（仅传递title字段内容）
>
> ```shell
> curl -X PUT 127.0.0.1:9200/articles/article/150000 -H 'Content-Type:application/json' -d '
> {
>   "title": "python必须是世界上最好的语言"
> }'
> ```
>
> - 而是要索引完整文档内容
>
> ```shell
> curl -X PUT 127.0.0.1:9200/articles/article/150000 -H 'Content-Type:application/json' -d '
> {
>   "article_id": 150000,
>   "user_id": 1,
>   "title": "python必须是世界上最好的语言",
>   "content": "确实如此",
>   "status": 2,
>   "create_time": "2019-04-03"
> }'
> ```
>
> - 注意返回值_version的变化

## 6. 删除文档

> ```shell
> curl -X DELETE 127.0.0.1:9200/articles/article/150000
> ```

## 7. 取回多个文档

> ```shell
> curl -X GET 127.0.0.1:9200/_mget -d '
> {
>   "docs": [
>     {
>       "_index": "articles",
>       "_type": "article",
>       "_id": 150000
>     },
>     {
>       "_index": "articles",
>       "_type": "article",
>       "_id": 150001
>     }
>   ]
> }'
> ```

