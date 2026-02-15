# IK中文分析器

> elasticsearch默认使用的是处理英文的分析器，如果向处理中文，就需要额外安装中文的分析器，最常用的是IK中文分析器

[TOC]

<!-- toc -->

### 1. IK分析器下载和安装

> centos测试开发镜像中已经安装好了IK中文分析器
>
> - 下载地址<https://github.com/medcl/elasticsearch-analysis-ik>
>
> - 将elasticsearch-analysis-ik-5.6.16.zip 复制到虚拟机中
>
>   ```shell
>   scp elasticsearch-analysis-ik-5.6.16.zip python@10.211.55.7:~/
>   ```
>
> - 安装
>
>   ```shell
>   sudo /usr/share/elasticsearch/bin/elasticsearch-plugin install file:///home/python/elasticsearch-analysis-ik-5.6.16.zip
>   ```
>
> - 重新启动elasticsearch
>
>   ```shell
>   sudo systemctl restart elasticsearch
>   ```

### 2. 测试分析器

> - ssh远程连接测试开发服务器
>
>   ```shell
>   ssh root@192.168.45.128
>   ```
>
> - 在命令行进行测试
>
>   - 查看elasticsearch默认的standard分析器的效果，在命令行中输入：
>
>   > ```shell
>   > curl -X GET 127.0.0.1:9200/_analyze?pretty -d '
>   > {
>   >   "analyzer": "standard",
>   >   "text": "我是&中国人"
>   > }'
>   > ```
>
>   - 查看ik分析器的效果：
>
>   > ```shell
>   > curl -X GET 127.0.0.1:9200/_analyze?pretty -d '
>   > {
>   >   "analyzer": "ik_max_word",
>   >   "text": "我是&中国人"
>   > }'
>   > ```

### 3. curl的使用

> curl是一个在命令行终端发送http请求的工具，功能上和python的requests模块类似
>
> ```shell
> curl -X http请求⽅方式 url -H 请求头字段 -d 请求体数据
> curl -X PUT 127.0.0.1:9200/article -H 'Content-Type:application/json' -d '{}'
> ```

