from flask import Flask



# 定义工厂函数:封装程序实例，可以根据参数的不同，创建不同的app
def create_applet_app(config_name=None):
    app = Flask(__name__)

    # 获取配置信息
    app.config.from_object(config_name)

    # 从models文件夹中导入sqlalchemy对象
    from models import db
    db.init_app(app)

    # 导入蓝图对象，注册蓝图
    from .user import user_bp
    app.register_blueprint(user_bp)
    from .mybooks import mybooks_bp
    app.register_blueprint(mybooks_bp)
    from .category import category_bp
    app.register_blueprint(category_bp)
    from .search import search_bp
    app.register_blueprint(search_bp)
    from .recommend import recommend_bp
    app.register_blueprint(recommend_bp)
    from .book import book_bp
    app.register_blueprint(book_bp)
    from .my import my_bp
    app.register_blueprint(my_bp)
    from .reader_config import config_bp
    app.register_blueprint(config_bp)

    # 导入请求钩子，用户的权限校验
    from lib.middlewares import before_request
    # 相当于@app.before_request
    app.before_request(before_request)

    return app




