
### 1.配置redis集群

* 安装Ruby

  ```shell
  # 下载ruby (1分钟)
  wget https://cache.ruby-lang.org/pub/ruby/2.6/ruby-2.6.1.tar.gz
  tar -zxvf ruby-2.6.1.tar.gz
  cd ruby-2.6.1
  ./configure
  # make 比较耗时(4分钟)
  sudo make & make install
  gem install redis
  ```

* 创建存放redis数据库的文件夹

  ```shell
  mkdir -p /home/python/redis/lib/7000
  mkdir -p /home/python/redis/lib/7001
  mkdir -p /home/python/redis/lib/7002
  mkdir -p /home/python/redis/lib/7003
  mkdir -p /home/python/redis/lib/7004
  mkdir -p /home/python/redis/lib/7005
  mkdir -p /home/python/redis/lib/6381
  mkdir -p /home/python/redis/lib/6380
  ```

* 分别启动redis

  ```python
  /usr/local/bin/redis-server /home/python/redis/lib/7000.conf
  ...
  ```
  
* 启动cluster集群

  ```shell
  # 拷贝redis-trib.rb命令到搜索路径下
  cp /root/redis-4.0.9/src/redis-trib.rb /usr/local/bin/
  # 创建集群
  redis-trib.rb create --replicas 1 127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005
  ```

* 测试redis集群

  ```shell
  redis-cli -c -p 7000
  ```

### 2.redis主从

* 使用脚本启动redis主从

  ```shell
  # vim /opt/redis-replication-start.sh
  
  #!/bin/bash
  /usr/local/bin/redis-server /etc/redis/6380.conf &
  /usr/local/bin/redis-server /etc/redis/6381.conf &
  /usr/local/bin/redis-sentinel /etc/redis/sentinel_16380.conf &
  /usr/local/bin/redis-sentinel /etc/redis/sentinel_16381.conf &
  /usr/local/bin/redis-sentinel /etc/redis/sentinel_16382.conf &
  ```

* 修改权限

  ```
  chmod +x /opt/redis-replication-start.sh
  chmod a+w sentinel_16380.conf
  chmod a+w sentinel_16381.conf
  chmod a+w sentinel_16382.conf
  ```
  
* 开机启动

  ```shell
  # vim /etc/init.d/leredis
  /opt/redis-replication-start.sh
  # 把docker 启动从mysql也加上
  service docker start
  docker container start  mysql
  ```

* 测试

  ```shell
  redis-cli -p 6381
  ```