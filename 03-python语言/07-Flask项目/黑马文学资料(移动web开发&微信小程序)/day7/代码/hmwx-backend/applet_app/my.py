# 导入蓝图
from flask import Blueprint,request,g,current_app,jsonify

# 导入登录验证装饰器
from lib.decoraters import login_required
# 导入模型类
from models import BrowseHistory,db

# 创建蓝图对象
my_bp = Blueprint('my',__name__,url_prefix='/my')

# 定义蓝图路由
@login_required
@my_bp.route('/histories')
def my_history():
    # 1.新建my.py文件，用来实现关于浏览记录的功能代码；
    # 2.创建蓝图、定义蓝图、注册蓝图
    # 3.导入登录验证装饰器
    # 4.获取参数，page和pagesize
    page = request.args.get('page',1,int)
    pagesize = request.args.get('pagesize',10,int)
    # 5.查询数据库浏览记录表，根据用户id查询，分页处理
    paginate = BrowseHistory.query.filter_by(user_id=g.user_id).paginate(page,pagesize,False)
    # 6.获取分页后的数据
    history_data = paginate.items
    items = []
    for item in history_data:
        # 使用关系引用book，从浏览记录表中，获取书籍表里的数据。
        items.append({
            'id':item.book.book_id,
            'title':item.book.book_name,
            'author':item.book.author_name,
            'status':item.book.status,
            'imgURL':'http://{}/{}'.format(current_app.config['QINIU_SETTINGS']['host'],item.book.cover),
            'lastTime':item.updated.strftime('%Y-%m-%d %H:%M:%S')
        })
    # 7.转成json，返回数据
    data = {
        'counts':paginate.total,
        'pagesize':pagesize,
        'pages':paginate.pages,
        'page':paginate.page,
        'items':items
    }
    return jsonify(data)

# 定义路由,实现浏览记录的删除
@login_required
@my_bp.route('/histories',methods=['DELETE'])
def delete_history():
    # 步骤：
    # 1.根据用户id、查询浏览记录表
    history_data = BrowseHistory.query.filter_by(user_id=g.user_id).all()
    # 2.遍历查询结果
    for data in history_data:
        db.session.delete(data)
    # 3.清除数据
    db.session.commit()
    # 4.返回结果
    return jsonify(msg='OK')
    pass
