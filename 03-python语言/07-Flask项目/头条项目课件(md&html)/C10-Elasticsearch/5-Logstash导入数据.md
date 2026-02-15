# Logstash导入数据

> 在django中，使用命令`python manage.py rebuild_index`来向ES中导入数据，今天我们来学习使用logstash 导入工具从mysql中导入数据，跟python haystack一样，它是用java实现的原生导入方式。

[TOC]

<!-- toc -->

## 1. Logstach下载安装

> - 第一步
>
> ```shell
> sudo rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
> ```
>
> - 第二步，在 /etc/yum.repos.d/ 中创建logstash.repo文件
>
> ```
> [logstash-6.x]
> name=Elastic repository for 6.x packages
> baseurl=https://artifacts.elastic.co/packages/6.x/yum
> gpgcheck=1
> gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
> enabled=1
> autorefresh=1
> type=rpm-md
> ```
>
> - 第三步，执行
>
> ```shell
> sudo yum install logstash
> cd /usr/share/logstash/bin/
> sudo ./logstash-plugin install logstash-input-jdbc
> sudo ./logstash-plugin install logstash-output-elasticsearch
> scp mysql-connector-java-8.0.13.tar.gz python@10.211.55.7:~/
> tar -zxvf mysql-connector-java-8.0.13.tar.gz # centos虚拟机请从这一步开始！！！
> ```
>
> - **注意，看上一行注释！！！**

## 2. 从MySQL导入数据到Elasticsearch

> - 创建配置文件logstash_mysql.conf
>
> ```
> input{
>      jdbc {  # java数据库访问的API接口
>          jdbc_driver_library => "/home/python/mysql-connector-java-8.0.13/mysql-connector-java-8.0.13.jar" # java连接操作mysql的包模块
>          jdbc_driver_class => "com.mysql.jdbc.Driver" 指明导入数据使用的类
>          jdbc_connection_string => "jdbc:mysql://127.0.0.1:3306/toutiao?tinyInt1isBit=false"
>          jdbc_user => "root"
>          jdbc_password => "mysql"
>          jdbc_paging_enabled => "true"  # 数据分页, 一共14W数据
>          jdbc_page_size => "1000"  # 每页1000条数据
>          jdbc_default_timezone =>"Asia/Shanghai"
>          statement => "select a.article_id as article_id,a.user_id as user_id, a.title as title, a.status as status, a.create_time as create_time,  b.content as content from news_article_basic as a inner join news_article_content as b on a.article_id=b.article_id"  # 联表查询, 尽量起别名,否则ES的字段名称会变为a.xx, 这样和mysql的字段名称会出现差异
>          use_column_value => "true"
>          tracking_column => "article_id"  # 如果希望ES的主键和mysql的一致,则需要设置追踪字段tracking_column, 同时设置use_column_value=true, 追踪的字段必须是递增的;如果设置use_column_value=false,文档id会根据添加时间自动递增生成
>          clean_run => true  # 从头取出mysql中的数据
>      }
> }
> output{
>       elasticsearch {
>          hosts => "127.0.0.1:9200"
>          index => "articles"
>          document_id => "%{article_id}"
>          document_type => "article"
>       }
>       stdout {  # 导入过程中以json形式显式的输出导入的内容
>          codec => json_lines  
>      }
> }
> ```
>
> - 执行数据导入命令
>
> ```shell
> sudo /usr/share/logstash/bin/logstash -f ./logstash_mysql.conf
> ```
>
> - **注意，centos虚拟机中一共14W条数；导入一点就够用了，赶紧ctrl+C吧！使劲按，多按几次！**

## 3. 查询文档数量

> ```shell
> curl -X GET localhost:9200/_cat/count?v
> curl -X GET localhost:9200/_cat/count/articles?v
> ```

