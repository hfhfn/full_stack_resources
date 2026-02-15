## Windows10下安装MySQL8.0

1：首先去官网下载安装包

下载地址：https://dev.mysql.com/downloads/mysql/

![img](https://images2018.cnblogs.com/blog/981899/201804/981899-20180429190040789-1279262126.png)

2：将解压文件解压到你安装的目录：E:\mysql-8-winx64 （我这是放在E盘根目录，不要放在有中文名字和空格的的目录下.例如 ![img](https://images2018.cnblogs.com/blog/981899/201804/981899-20180429190546139-1980212483.png))

3：在mysql-8-winx64文件夹下面新建一个my.ini文件

![img](https://images2018.cnblogs.com/blog/981899/201804/981899-20180429190657895-4896444.png)

- my.ini 文件内容：

```
[mysqld]
# 设置3306端口
port=3306
# 设置mysql的安装目录
basedir=E:\\mysql-8
# 设置mysql数据库的数据的存放目录
datadir=E:\\mysql-8\\data
# 允许最大连接数
max_connections=200
# 允许连接失败的次数。这是为了防止有人从该主机试图攻击数据库系统
max_connect_errors=10
# 服务端使用的字符集默认为UTF8
character-set-server=utf8
# 创建新表时将使用的默认存储引擎
default-storage-engine=INNODB
[mysql]
# 设置mysql客户端默认字符集
default-character-set=utf8
[client]
# 设置mysql客户端连接服务端时默认使用的端口
port=3306
default-character-set=utf8
```

- 手动创建安装目录和mysql数据存放目录(如果创建不同的目录，需要修改my.ini文件中对应的路径)
  - E:\\mysql-8
  - E:\\mysql-8\\data

4：配置系统环境（在系统变量中新建MYSQL_HOME）

![img](https://images2018.cnblogs.com/blog/981899/201804/981899-20180429191129805-1900374880.png)

在系统变量的path中添加%MYSQL_HOME%\bin

5：以***管理员的身份***打开cmd窗口跳转路径到E:\mysql-8.0.11-winx64\bin

初始化命令mysqld --initialize --user=mysql --console

初始化完成之后，会生成一个临时密码这里需要注意把临时密码记住

![img](https://images2018.cnblogs.com/blog/981899/201804/981899-20180429191948310-1685290947.png)

- 接着就是输入mysqld -install进行服务的添加
- 输入net start mysql启动服务
- 输入mysql -u root -p进行登录数据库，这时提示需要密码，然后就是用你上面的密码登录
- 修改权限和密码

```
# 1.修改mysql密码 (123456可以改为自己的密码)
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456';

# 2.修改mysql的root用户权限
update mysql.user set host = '%' where user = 'root';

# 3.刷新权限
flush privileges;
```

