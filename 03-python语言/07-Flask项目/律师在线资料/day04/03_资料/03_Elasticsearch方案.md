### Elasticsearch方案

#### 1, 概述

- 特点: 
  - 1, Elasticsearch是一个基于Lucene库的搜索引擎。
  - 2, Elasticsearch使用Java开发, 能在python,php等其他语言中使用
  - 3, 支持倒排序索引
    - ​	![image-20191116223949444](03_Elasticsearch方案.assets/image-20191116223949444.png)
  - 4, 可以配合logstash进行数据处理
- 使用es的公司
  - 1, 维基百科(Wikipedia): 高亮片段全文检索
  - 2, 卫报: 将社交数据和日志信息, 实时检索用户信息反馈到管理员
  - 3, Stack Overflow: 全文检索搜索答案
  - 4, Github: 使用ES对1300亿行代码进行检索
  - 5, ...
- 下载地址:
  - https://www.elastic.co/cn/downloads/past-releases#elasticsearch
  - 选择:

#### 2,安装

- 1, 下载 5.6.16版本稳定

- 2, 解压至指定目录
  - ```python
    tar zxvf elasticsearch-5.6.16.tar.gz -C /home/python
    ```

- 3, 运行

  - ```python
    ./bin/elasticsearch
    
    或者后台运行
    bin/elasticsearch -d
    ```

- 4, 测试

  - ```python
    curl 127.0.0.1:9200
    ```

- 注意点:
  - 如果要修改启动的端口和ip
  - 编辑该文件: /home/python/elasticsearch-5.6.16/config/elasticsearch.yml

#### 3, elasticsearch-ik中文分析器

- 1, 下载https://github.com/medcl/elasticsearch-analysis-ik/releases

  - 注意点: 下载的分词器, 需要和es的版本保持一致

- 2, 安装

  - ```python
    sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install file:///home/python/elasticsearch-analysis-ik-5.6.16.zip
    ```

- 3, 测试分词器

  - ```python
    curl -X GET 172.16.12.134:9200/_analyze?pretty -d '
    {
      "analyzer": "standard",
      "text": "我是&中国人"
    }'
    
    curl -X GET 172.16.12.134:9200/_analyze?pretty -d '
    {
      "analyzer": "ik_max_word",
      "text": "我是&中国人"
    }'
    ```

- 注意点:

  - standard: 按照汉字拆分
  - ik_max_word: 按照单词格式划分

  

#### 4, 使用测试

- 1, 查看索引库

  - ```python
    curl 127.0.0.1:9200/_cat/indices
    ```

- 2, 创建索引库建立

  - ```python
    // 文章索引
    curl -X PUT 172.16.12.134:9200/articles -H 'Content-Type: application/json' -d'
    {
       "settings" : {
            "index": {
                "number_of_shards" : 3,
                "number_of_replicas" : 1
            }
       }
    }
    '
    ```

- 3, 创建索引表

  - ```python
    curl -X PUT 172.16.12.134:9200/articles/_mapping/article -H 'Content-Type: application/json' -d'
    {
         "_all": {
              "analyzer": "ik_max_word"
          },
          "properties": {
              "article_id": {
                  "type": "long",
                  "include_in_all": "false"
              },
              "user_id": {
                  "type": "long",
                  "include_in_all": "false"
              },
              "title": {
                  "type": "text",
                  "analyzer": "ik_max_word",
                  "include_in_all": "true",
                  "boost": 2
              },
              "content": {
                  "type": "text",
                  "analyzer": "ik_max_word",
                  "include_in_all": "true"
              },
              "status": {
                  "type": "integer",
                  "include_in_all": "false"
              },
              "create_time": {
                  "type": "date",
                  "include_in_all": "false"
              }
          }
    }
    '
    ```

- 4, 查看映射

  - ```python
    curl 172.16.12.134:9200/articles/_mapping/article?pretty
    ```

- 5, 修改映射

  - ```python
    curl -X PUT 172.16.12.134:9200/articles_v2 -H 'Content-Type: application/json' -d'
    {
       "settings" : {
          "index": {
              "number_of_shards" : 3,
              "number_of_replicas" : 1
           }
       }
    }
    '
    
    curl -X PUT 172.16.12.134:9200/articles_v2/_mapping/article -H 'Content-Type: application/json' -d'
    {
         "_all": {
              "analyzer": "ik_max_word"
          },
          "properties": {
              "article_id": {
                  "type": "long",
                  "include_in_all": "false"
              },
              "user_id": {
                   "type": "long",
                  "include_in_all": "false"
              },
              "title": {
                  "type": "text",
                  "analyzer": "ik_max_word",
                  "include_in_all": "true",
                  "boost": 2
              },
              "content": {
                  "type": "text",
                  "analyzer": "ik_max_word",
                  "include_in_all": "true"
              },
              "status": {
                  "type": "byte",
                  "include_in_all": "false"
              },
              "create_time": {
                  "type": "date",
                  "include_in_all": "false"
              }
          }
    }
    '
    ```

- 重新索引数据

  - ```python
    curl -X POST 172.16.12.134:9200/_reindex -H 'Content-Type:application/json' -d '
    {
      "source": {
        "index": "articles"
      },
      "dest": {
        "index": "articles_v2"
      }
    }
    '
    ```

#### 5,elasticsearch专用词库

- 目的: 比如举个新出的网红词汇, 如何进行索引
  - 1, 测试, 不能识别

    - ```python
      curl -X GET 172.16.12.134:9200/_analyze?pretty -d '{ "analyzer": "ik_max_word", "text": "盘它"}'
      ```

  - 2, 编辑配置引用(/home/python/elasticsearch-5.6.16/config/analysis-ik/IKAnalyzer.cfg.xml)

    - ```python
      ...
      <entry key="ext_dict">lawyer_ol/my_dict.dic</entry>
      ...
      ```

  - 3, 新建文件(/home/python/elasticsearch-5.6.16/config/analysis-ik/lawyer_ol/my_dict.dic)

    - ```python
      蓝瘦
      蓝瘦香菇
      盘它
      ```

#### 6,elasticsearch停用词库

- 目的: 为了去过滤一些语气词之类的

- 1, 测试

  - ```python
    curl -X GET 172.16.12.134:9200/_analyze?pretty -d '{ "analyzer": "ik_max_word", "text": "蓝瘦香菇哈"}'
    ```

  2, 编辑配置引用(/home/python/elasticsearch-5.6.16/config/analysis-ik/IKAnalyzer.cfg.xml)

  - ```python
    也
    了
    仍
    从
    以
    使
    ...
    哈
    ```

#### 7,elasticsearch中文自动补全

- 1, 建立索引库

  - ```python
    curl -X PUT 172.16.12.134:9200/completions -H 'Content-Type: application/json' -d'
    {
      "settings" : {
        "index": {
          "number_of_shards" : 3,
          "number_of_replicas" : 1
        }
      }
    }'
    ```

- 2, 建立索引表

  - ```python
    curl -X PUT 172.16.12.134:9200/completions/_mapping/words -H 'Content-Type: application/json' -d'
    {
      "words": {
        "properties": {
          "suggest": {
            "type": "completion",
            "analyzer": "ik_max_word"
          }
        }
      }
    }'
    ```

- 3, 导入数据

  - ```python
    sudo /home/python/logstash-6.2.4/bin/logstash -f ./logstash_mysql_completion.conf
    ```

- 4, 查看数据总条数

  - ```python
    curl 172.16.12.134:9200/completions/words/_count?pretty
    ```

- 5, 搜索测试

  - ```python
    curl 172.16.12.134:9200/completions/words/_search?pretty -d '
    {
      "suggest": {
        "title-suggest" : {
          "prefix" : "中",
          "completion" : {
          		"field" : "suggest"
          }
        }
      }	
    }'
    ```