# Flask介绍

[TOC]

<!-- toc -->

## 1 学习Flask框架的原因

> 2018 Python官方年度调研报告显示Flask与Django为Python Web开发使用最主要的两个框架。
>
> ![框架占比](/images/2018年Web框架占比.png)

## 2 Flask

> ![flask](/images/flask.png)
>
> Flask诞生于2010年，是Armin ronacher（人名）用 Python 语言基于 Werkzeug 工具箱编写的轻量级Web开发框架。
>
> Flask 本身相当于一个内核，其他几乎所有的功能都要用到扩展（邮件扩展Flask-Mail，用户认证Flask-Login，数据库Flask-SQLAlchemy），都需要用第三方的扩展来实现。比如可以用 Flask 扩展加入ORM、窗体验证工具，文件上传、身份验证等。Flask 没有默认使用的数据库，你可以选择 MySQL，也可以用 NoSQL。
>
> 其 WSGI 工具箱采用 Werkzeug（路由模块），模板引擎则使用 Jinja2。这两个也是 Flask 框架的核心。
>
> **最新版本 1.0.2**

## 3 框架对比

> - 框架轻重
>
>   - 重量级的框架：为方便业务程序的开发，提供了丰富的工具、组件，如Django
>
>   - 轻量级的框架：只提供Web框架的核心功能，自由、灵活、高度定制，如Flask、Tornado
>
> - 与Django对比,django提供了：
>
>   > django-admin快速创建项目工程目录
>   >
>   > manage.py 管理项目工程
>   >
>   > orm模型（数据库抽象层）
>   >
>   > admin后台管理站点
>   >
>   > 缓存机制
>   >
>   > 文件存储系统
>   >
>   > 用户认证系统
>
>   - 而这些，flask都没有，都需要扩展包来提供

## 4 常用扩展包

> 扩展列表：http://flask.pocoo.org/extensions/
>
> - Flask-SQLalchemy：操作数据库；
> - Flask-script：插入脚本；
> - Flask-migrate：管理迁移数据库；
> - Flask-Session：Session存储方式指定；
> - Flask-WTF：表单；
> - Flask-Mail：邮件；
> - Flask-Bable：提供国际化和本地化支持，翻译；
> - Flask-Login：认证用户状态；
> - Flask-OpenID：认证；
> - **Flask-RESTful：开发REST API的工具；**
> - Flask-Bootstrap：集成前端Twitter Bootstrap框架；
> - Flask-Moment：本地化日期和时间；
> - Flask-Admin：简单而可扩展的管理接口的框架

## 5 Flask文档

> - 中文文档（[http://docs.jinkan.org/docs/flask/](http://docs.jinkan.org/docs/flask/)）
>
> - 英文文档（[http://flask.pocoo.org/docs/1.0/](http://flask.pocoo.org/docs/1.0/)）