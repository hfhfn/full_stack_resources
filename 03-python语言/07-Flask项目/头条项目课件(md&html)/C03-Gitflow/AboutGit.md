# Gitflow工作流在项目中的使用

[TOC]

<!-- toc -->

## 1. Gitflow工作流分支命名

> 分支命名的通用约定
>
> | 分支名称 | 作用                       |
> | -------- | -------------------------- |
> | master   | 迭代历史分支               |
> | dev      | 集成最新开发特性的活跃分支 |
> | f_xxx    | feature 功能特性开发分支   |
> | b_xxx    | bug修复分支                |
> | r_xxx    | release 版本发包分支       |

## 2. 项目中具体使用

> 做好git以及gitlab相关安装及配置操作后，按如下步骤操作

### 2.1 同步远程分支

> 本步骤只有在初次执行，完成一次分支的提交和推送后，不再本步骤，直接从下一步开始执行
>
> ```shell
> git init # 本地初始化
> git remote add origin git@git.meiduo.site:bt43/toutiao.git # 添加远程分支，从gitlab上复制过来
> git fetch # 同步更新，等一会
> git branch -a # 查看全部分支，此时没有本地分支
> git checkout -b dev origin/dev # 创建本地dev分支 并且和远程的dev分支相对应
> git pull # 从远程的dev分支拉取代码到本地dev分支
> ```

### 2.2 创建本地开发分支

> ```shell
> git checkout -b f_test # 创建并切换到本地某一个开发分支，开始进行开发工作
> ```

### 2.3 推送本地分支到远程

> 两种方式
>
> - 方式一
>
>   - pycharm点击项目文件夹，ctrl+k 填写提交说明并提交
>   - pycharm点击项目文件夹，ctrl+shift+k 推送到远程分支
>
> - 方式二
>
>   ```shell
>   git status # 查看当前git相关状态：当前本地分支，对应远程分支，二者区别，是否有commit的内容
>   git add . # 添加内容到工作区，注意后边有个点，表示当前路径下全部
>   git commit -m 'xxx' # 提交，并自定义本次提交的描述
>   git push origin f_test:f_test # 推送本地分支到远程
>   ```

### 2.4 提交合并请求

> 在gitlab网站上做如下操作：
>
> 1. 登录gitlab网站，进入项目主页，点击`Merge Requests`后，再点击`New merge request`提交新的合并请求
> 2. 分别选择具体的`Source branch`分支和`Target branch`分支，点击`Compare branches and continue`进入发起提交页面
> 3. 填写发起分支的`titel`和`Description`（合并分支请求的标题和描述内容）后，点击`Submit merge request`发起合并请求

### 2.5 删除本地分支并更新远端分支列表

> ```shell
> git checkout dev # 切换到本地dev
> git pull # 本地dev和远程同步
> git branch -d f_test # 删除本地分支
> git remote update origin -p # 更新远端列表
> ```

## 3. Confict冲突解决

> 如果提交合并请求中的代码和合并目标的代码产生了冲突，解决的方式有两种
>
> - 方式一
>
>   > 1. 获取最新代码
>   >
>   > ```shell
>   > git fetch
>   > ```
>   >
>   > 2. 对比代码
>   >
>   > ```shell
>   > git diff origin/dev
>   > ```
>   >
>   > 3. 修改冲突地方后提交并推送代码
>   > 4. 发起合并请求
>
> - 方式二
>
>   > 1. 将目标分支的代码拉取到本地分支，并合并
>   >
>   > ```shell
>   > git pull origin dev # 拉取origin/dev代码到当前分支
>   > ```
>   >
>   > 2. 查看冲突代码
>   >
>   > ```shell
>   > git status
>   > ```
>   >
>   > 3. 修改冲突代码后提交并推送代码
>   > 4. 发起合并请求
>   
> - 注意，方式二对md等格式的文档支持并不好，无法显示md文档中的冲突