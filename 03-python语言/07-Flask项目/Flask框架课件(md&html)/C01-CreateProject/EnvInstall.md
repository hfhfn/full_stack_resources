# 环境安装

## 1. 复习虚拟环境和pip的命令

> ```shell
> # 虚拟环境
> mkvirtualenv  # 创建虚拟环境
> rmvirtualenv  # 删除虚拟环境
> workon  # 进入虚拟环境、查看所有虚拟环境
> source /[path]/env_name/bin/activate # 或者用source来切入虚拟环境
> deactivate  # 退出虚拟环境
> 
> # pip
> pip install  # 安装依赖包
> pip uninstall  # 卸载依赖包
> pip list  # 查看已安装的依赖包
> pip freeze  # 冻结当前环境的依赖包
> ```

## 2. 创建虚拟环境

> 注意需要联网
>
> ```shell
> whereis python # 查看python解释器执行文件的路径
> mkvirtualenv venv_name --python=/usr/bin/python3.6 # 指定python版本来创建虚拟环境
> ```

## 3. 安装Flask

> 默认安装flask最新版本，注意需要联网
>
> ```shell
> pip install flask
> ```

