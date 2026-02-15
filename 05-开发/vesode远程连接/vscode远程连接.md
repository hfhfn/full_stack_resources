# vscode远程连接

[TOC]

### 1、安装vscode的sftp插件，如图所示：

![Snip20190423_2](./src/Snip20190423_2.png)



### 2、创建目录nginx

![Snip20190423_3](./src/Snip20190423_3.png)



### 2、配置远程连接插件

#### 在创建的目录下使用快捷键

windows系统快捷键

`ctrl + shift + P`

Mac系统快捷键

`command + shift +P`

![Snip20190423_5](./src/Snip20190423_5.png)

#### 选择配置后按如下图配置

![Snip20190423_7](./src/Snip20190423_7.png)

### 3、进入ubuntu系统安装openssh-server

```shell
sudo apt install openssh-server
```



### 4、设置ubuntu的root账户密码

```shell
sudo passwd root
```

![Snip20190423_8](./src/Snip20190423_8.png)



### 5、设置允许root账户远程登录

打开ssh配置文件

```shell
 sudo vi /etc/ssh/sshd_config 
```

按照如图所示修改ssh配置

![Snip20190423_11](./src/Snip20190423_11.png)

重启ssh服务

```shell
sudo service ssh restart 
```



### 6、下载远程服务器文件

![Snip20190423_9](./src/Snip20190423_9.png)

输入密码开始下载远程文件

![Snip20190423_10](/Users/august/Desktop/vesode/src/Snip20190423_10.png)

下载之后文件目录如下

![Snip20190423_12](./src/Snip20190423_12.png)

### 7、打开vscode终端远程登录服务器

![Snip20190423_14](./src/Snip20190423_14.png)

![Snip20190423_15](./src/Snip20190423_15.png)