# ToutiaoWeb虚拟机使用说明

* 作为项目的开发环境
* 黑窗口 无GNOME  模拟企业中的开发服务器环境

- CentOS7.2

- 开机前先将虚拟机调成NAT模式

- 虚拟机占用内存4G，如果主机内存不足，可启动前将内存占用调为2G

- ssh远程连接 `ssh python@自己的ip地址`

- 用户名 密码
  - 系统
    - root  -> chuanzhi
    - python -> chuanzhi
  - MySQL
    - root -> mysql
  
- 端口
  - MySQL (mariadb)
    - master -> 3306
    - slave -> 8306   (mysql -uroot -p -h 127.0.0.1 --port=8306)
    
  - Redis
    
    > 虚拟机中配置的redis禁止外部访问
    
    - cluster  -> 7000  7001 7002 7003 7004 7005
    - master & slave -> 6380 6381
    - sentinel -> 26380 26381 26382
    
  - Elasticsearch 5
    
    - 9200
  
- Python 虚拟环境 
  - 进入虚拟环境 source /home/python/.virtualenvs/toutiao/bin/activate
  - 退出虚拟环境 deactivate
  
- 关机 sudo shutdown now

- 重启 reboot

- 修改时间为北京时间 ntpdate ntp.api.bz

