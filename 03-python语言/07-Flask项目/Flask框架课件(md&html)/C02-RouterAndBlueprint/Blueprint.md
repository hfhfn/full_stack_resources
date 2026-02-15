# 蓝图

> - 思考：
>   - 在一个Flask 应用项目中，如果业务视图过多，可否将以某种方式划分出的业务单元单独维护，将每个单元用到的视图、静态文件、模板文件等独立分开？
>   - 例如从业务角度上，可将整个应用划分为用户模块单元、商品模块单元、订单模块单元，如何分别开发这些不同单元，并最终整合到一个项目应用中？
> - 蓝图从项目代码结构上解决了多人合作，共同开发的问题

[TOC]
<!-- toc -->

## 1. 使用蓝图

> 在Flask中，使用蓝图Blueprint来分模块来进行组织管理。
>
> - 蓝图实际可以理解为是一个存储一组视图方法的容器对象，其具有如下特点：
>   - 一个flask_app应用可以具有多个Blueprint
>   - 可以将一个Blueprint注册到任何一个未使用的URL下比如 “/user”、“/goods”
>   - Blueprint可以单独具有自己的模板、静态文件或者其它的通用操作方法
>   - 在一个应用初始化时，就应该要注册需要使用的Blueprint
>   - 但是一个Blueprint并不是一个完整的应用，它不能独立于应用运行，而必须要注册到某一个应用中。

## 2. 使用方式

>  使用蓝图可以分为三个步骤
>
> 1. 创建一个蓝图对象
> 2. 在这个蓝图对象上进行操作，如：注册路由,指定静态文件夹,注册模版过滤器等
> 3. 在应用对象上注册这个蓝图对象
>
> ```python
> from flask import Flask, Blueprint
> 
> # step 1. 创建一个蓝图对象
> user_bp = Blueprint('user', __name__) # user为蓝图的自定义名字
> 
> # step 2. 定义一个蓝图对象的视图函数
> @user_bp.route('/blue')
> def user_profile():
> 	return 'this is blueprint'
> 
> # step 3. 实例化flask app，并注册蓝图对象
> app = Flask(__name__)
> app.register_blueprint(user_bp) # 注册蓝图对象
> 
> @app.route('/')
> def route_map():
>     return 'this is index'
> 
> if __name__ == '__main__':
>     app.run(debug=True)
> ```

### 2.1 单文件蓝图

> 如上面的代码，可以将创建蓝图对象与定义视图放到一个文件中 。

### 2.2 目录（包）蓝图

> 对于一个打算包含多个文件的蓝图，通常将创建蓝图对象放到Python包的`__init__.py`文件中
>
> ```shell
>  ---- project # 工程目录
>           |---- main.py # 启动文件
>           |---- user  #用户蓝图文件夹
>           |      |--- __init__.py  # 此处创建蓝图对象
>           |      |--- user_views.py  # 具体的视图函数所在文件
>           |      |--- ...
>           |
>           |---- goods # 商品蓝图文件夹
>           |      |--- __init__.py
>           |      |--- goods_views.py  # 具体的视图函数所在文件
>           |      |--- ...
>           |...
> ```
>
> 接下来我们就按照上边的工程目录来实践一下，来切身感受一下蓝图的效果

#### 2.2.1 `main.py`

> ```python
>from flask import Flask
>   from user import user_bp
>   from goods import goods_bp
>   
>   app = Flask(__name__)
>   app.register_blueprint(user_bp)
>   app.register_blueprint(goods_bp)
>   
>   @app.route("/")
>   def index():
>      return "index"
>   
>    if __name__ == '__main__':
>      app.run(debug=True)
>   ```

#### 2.2.2 `user/__init__.py`

> ```python
>from flask import Blueprint
>   user_bp = Blueprint('user', __name__)
>   from user import user_views # 思考这行代码的作用
>   ```

#### 2.2.3 `user/user_views.py`

> ```python
>from user import user_bp
>   @user_bp.route('/user')
>   def user():
>   	return 'user'
>   ```

####2.2.4 `goods/__init__.py`

> ```python
>from flask import Blueprint
>   goods_bp = Blueprint('goods', __name__)
>   from goods import goods_views # 又来了...
>   ```

#### 2.2.5 `goods/goods_views.py`

> ```python
>from goods import goods_bp
>   @goods_bp.route('/goods')
>   def goods():
>   	return 'goods'
>   ```

## 3. 蓝图中自定义参数

> - 定义url前缀
> - 指定蓝图内部静态文件夹
> - 指定蓝图内部模板目录

### 3.1 指定蓝图的url前缀

> 在应用中注册蓝图时使用`url_prefix`参数指定
>
> - `http://127.0.0.1:5000`
> - `http://127.0.0.1:5000/bp/blue`
>
> ```python
> import json
> from flask import Flask, Blueprint
> 
> bp=Blueprint('bp', __name__)
> 
> @bp.route('/blue')
> def blue_view():
> 	return 'this is blueprint'
> 
> app = Flask(__name__)
> # 注册蓝图，url_prefix参数指定url前缀
> app.register_blueprint(bp, url_prefix='/bp')
> 
> @app.route('/')
> def route_map():
>     """返回所有视图网址"""
>     rules_iterator = app.url_map.iter_rules()
>     return json.dumps({rule.endpoint: rule.rule for rule in rules_iterator})
> 
> if __name__ == '__main__':
>     app.run(debug=True)
> ```

### 3.2 指定蓝图内部静态文件夹

#### 3.2.1 注册蓝图的静态目录

> 和应用对象不同，蓝图对象创建时不会默认注册静态目录的路由。需要我们在 创建时指定 static_folder 参数。
>
> ```python
> import json
> from flask import Flask, Blueprint
> # static_folder='bp_static' 指定蓝图内部静态文件夹
> bp=Blueprint('bp', __name__, static_folder='bp_static')
> 
> @bp.route('/blue')
> def blue_view():
> 	return 'this is blueprint'
> 
> app = Flask(__name__)
> # 注册蓝图，url_prefix参数指定url前缀
> app.register_blueprint(bp, url_prefix='/bp')
> 
> @app.route('/')
> def route_map():
>     """返回所有视图网址"""
>     rules_iterator = app.url_map.iter_rules()
>     return json.dumps({rule.endpoint: rule.rule for rule in rules_iterator})
> 
> if __name__ == '__main__':
>     app.run(debug=True)
> ```
>
> 现在就可以使用`/bp/bp_static/<filename> `访问`bp_static`目录下的静态文件了。

#### 3.2.2 设置蓝图静态文件的访问路径

> 也可通过`static_url_path`改变访问路径
>
> ```python
> import json
> from flask import Flask, Blueprint
> # static_folder='bp_static' 指定蓝图内部静态文件夹
> # static_url_path='/lib' 改变访问路径为 /bp/lib/<filename>
> bp=Blueprint('bp', __name__, static_folder='bp_static', static_url_path='/lib')
> 
> @bp.route('/blue')
> def blue_view():
> 	return 'this is blueprint'
> 
> app = Flask(__name__)
> # 注册蓝图，url_prefix参数指定url前缀
> app.register_blueprint(bp, url_prefix='/bp')
> 
> @app.route('/')
> def route_map():
>     """返回所有视图网址"""
>     rules_iterator = app.url_map.iter_rules()
>     return json.dumps({rule.endpoint: rule.rule for rule in rules_iterator})
> 
> if __name__ == '__main__':
>     app.run(debug=True)
> ```

### 3.3 蓝图内部模板目录

> 蓝图对象默认的模板目录为系统的模版目录，可以在创建蓝图对象时使用 template_folder 关键字参数设置模板目录
>
> `http://127.0.0.1:5000/bp/blue`
>
> ```python
> import json
> from flask import Flask, Blueprint
> # static_folder='bp_static' 指定蓝图内部静态文件夹
> # static_url_path='/lib' 改变访问路径为 /bp/lib/<filename>
> # template_folder='bp_templates' 改变蓝图的模板目录
> bp=Blueprint('bp', __name__,
>              static_folder='bp_static',
>              static_url_path='/lib',
>              template_folder='bp_templates')
> 
> @bp.route('/blue')
> def blue_view():
> 	return 'this is blueprint'
> 
> app = Flask(__name__)
> # 注册蓝图，url_prefix参数指定url前缀
> app.register_blueprint(bp, url_prefix='/bp')
> 
> @app.route('/')
> def route_map():
>     """返回所有视图网址"""
>     rules_iterator = app.url_map.iter_rules()
>     return json.dumps({rule.endpoint: rule.rule for rule in rules_iterator})
> 
> if __name__ == '__main__':
>     app.run(debug=True)
> ```

### 3.4 拓展1:蓝图自定义名称的作用

> 蓝图自定义名称可以帮助我们做url_for跳转等工作
>
> ```python
> from flask import Flask, Blueprint, render_template, url_for
> 
> bp=Blueprint('bp', __name__,
>              static_folder='bp_static',
>              static_url_path='/lib',
>              template_folder='bp_templates')
> 
> @bp.route('/blue')
> def blue_view():
> 	return render_template('3.html')
> 
> app = Flask(__name__)
> app.register_blueprint(bp, url_prefix='/bp')
> 
> @app.route('/')
> def index():
>     # url_for函数，通过视图函数明获取它对应的url字符串
>     # 某个视图url的字符串 = flask.url_for('视图函数名')
>     # 蓝图的某个视图url的字符串 = flask.url_for('自定义蓝图名.视图函数名')
>     return url_for('bp.blue_view') # '/bp/blue'
> 
> if __name__ == '__main__':
>     app.run(debug=True)
> ```

### 3.5 拓展2:蓝图设置请求钩子,只会监听该蓝图注册的路由

> 关于`请求钩子`，我们会在后面学习
>
> ```python
> from flask import Flask, Blueprint
> 
> bp=Blueprint('bp', __name__)
> 
> # 蓝图设置请求钩子，只会监听该蓝图注册的路由
> # 在接收到请求之后，运行bp蓝图的视图函数之前运行
> @bp.before_request
> def before_request_func():
>     print('只有访问蓝图的url才会看见我！')
> 
> @bp.route('/blue')
> def blue_view():
> 	return 'blue'
> 
> app = Flask(__name__)
> app.register_blueprint(bp, url_prefix='/bp')
> 
> @app.route('/')
> def index():
>     return 'index'
> 
> if __name__ == '__main__':
>     app.run(debug=True)
> ```

