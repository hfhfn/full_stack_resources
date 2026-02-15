## 一、索引库操作

#### 1.1、索引库的增删查

 添加头条项目文章索引库


            curl -X PUT 127.0.0.1:9200/qusts -H 'Content-Type: application/json' -d'
            {
               "settings" : {
                    "index": {
                        "number_of_shards" : 3,
                        "number_of_replicas" : 1
                    }
               }
            }
            '

重新查看可看到qusts索引库：

``````
[python@toutiao-web ~]$ curl 127.0.0.1:9200/_cat/indices
yellow open articles Od6OeobVSma2yNUaCMi2Qw 3 1 0 0 486b 486b
``````

删除索引库：

```
curl -X DELETE 127.0.0.1:9200/articles
```



#### 1.2、数据库类型映射(数据表)的创建与查询


     创建：
    	curl -X PUT 127.0.0.1:9200/qusts/_mapping/qust -H 'Content-Type: application/json' -d'
        {
             "_all": {
                  "analyzer": "ik_max_word"
              },
              "properties": {
                  "qustion_id": {
                      "type": "long",
                      "include_in_all": "false"
                  },
                  "asker_id": {
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
                  "expertise_id": {
                      "type": "long",
                      "include_in_all": "false"
                  },
                  "city_id": {
                      "type": "long",
                      "include_in_all": "false"
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
    查询：
    
        curl 127.0.0.1:9200/qusts/_mapping/qust?pretty  


​       

#### 1.3、Logstash导入数据

Logstach安装(课件2.6)

创建配置文件logstash_mysql.conf

``````
input{
    jdbc {
        jdbc_driver_library => "/home/python/mysql-connector-java-8.0.13/mysql-connector-java-8.0.13.jar"
        jdbc_driver_class => "com.mysql.jdbc.Driver"
        jdbc_connection_string => "jdbc:mysql://127.0.0.1:3306/lawyer_ol?tinyInt1isBit=false"
        jdbc_user => "root"
        jdbc_password => "mysql"
        jdbc_paging_enabled => "true"
        jdbc_page_size => "1000"
        jdbc_default_timezone =>"Asia/Shanghai"
        statement => "select a.qust_id as qustion_id,a.user_id as asker_id, a.title as title, a.expertise_id as expertise_id, a.city_id as city_id, a.status as status, a.create_time as create_time,  b.content as content from question_basic as a inner join question_content as b on a.qust_id=b.qust_id"
        use_column_value => "true"
        tracking_column => "qust_id"
        clean_run => true
    }
}
output{
    elasticsearch {
        hosts => "127.0.0.1:9200"
        index => "qusts"
        document_id => "%{qustion_id}"
        document_type => "qust"
    }
    stdout {
        codec => json_lines
    }
}
``````

    解压mysql-connector-java-8.0.13.zip文件， 得到mysql-connector-java-8.0.13目录
    
        tar -zxvf mysql-connector-java-8.0.13.tar.gz
    
    # 执行：
    sudo /home/python/logstash-6.2.4/bin/logstash -f /home/python/logstash_mysql.conf


​    
​     # 等到显示有一定数据的时候，就可以按Ctrl+C来停止，我们只需要插入一部分测试数据即可


#### 1.4、查询数据


        根据文档ID
    
            curl -X GET 127.0.0.1:9200/qusts/qust/1?pretty
            curl -X GET 127.0.0.1:9200/qusts/qust/1?_source=content,asker_id\&pretty
            curl -X GET 127.0.0.1:9200/qusts/qust/1?_source=false\&pretty



```
查询一共有多少条
curl -X GET 127.0.0.1:9200/qusts/qust/_count?pretty
结果：
{
  "count" : 19803,
  "_shards" : {
    "total" : 3,
    "successful" : 3,
    "skipped" : 0,
    "failed" : 0
  }
}

```

​        查询所有

            curl -X GET 127.0.0.1:9200/qusts/qust/_search?_source=content,asker_id\&pretty
    
            默认查询出10条数据
    
        分页查询
            curl -X GET 127.0.0.1:9200/qusts/qust/_search?_source=content,asker_id\&size=3\&pretty


        全文检索：
            curl -X GET 127.0.0.1:9200/qusts/qust/_search?q=content:%27交通%27\&_source=content,qustion_id\&pretty



            curl -X GET 127.0.0.1:9200/qusts/qust/_search?q=content:%27贷款%27\&_source=content,qustion_id\&pretty


            curl -X GET 127.0.0.1:9200/qusts/qust/_search?q=_all:%27工伤%27\&_source=content,qustion_id\&pretty



from 从哪一条起，size查询多少条

``````
curl -X GET 127.0.0.1:9200/qusts/qust/_search?_source=content,user_id\&size=3\&from=10\&pretty
``````

