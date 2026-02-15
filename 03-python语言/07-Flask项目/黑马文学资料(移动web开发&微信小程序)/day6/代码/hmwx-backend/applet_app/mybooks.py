# 导入随机数模块
import random
# 导入蓝图对象
from flask import Blueprint,g,current_app,jsonify

# 导入登录验证装饰器
from lib.decoraters import login_required
# 导入模型类书架
from models import BookShelf,Book,db,User,BookChapters,ReadRate

# 书架
# 创建蓝图对象
mybooks_bp = Blueprint('mybook',__name__,url_prefix='/mybooks')

# 定义路由，书架列表
@login_required
@mybooks_bp.route("/")
def mybooks_list():
    # 1.添加登录验证装饰器
    user_id = g.user_id
    # 2.默认查询书架中的所有书籍数据，排序
    mybooks = BookShelf.query.filter_by(user_id=user_id).order_by(BookShelf.created.desc()).all()
    # 定义临时列表，存储数据
    data = []
    # 3.判断查询结果
    if not mybooks:
        # 如果书架没有书籍，随机挑选5本书籍，存入书架中
        books = Book.query.all()
        books_list = random.sample(books,5)
        for bk in books_list:
            book_shelf = BookShelf(
                user_id=user_id,
                book_id=bk.book_id,
                book_name=bk.book_name,
                cover=bk.cover
            )
            # 提交数据
            db.session.add(book_shelf)
            # 添加的七牛云存储的图片的绝对路径：七牛云的空间域名+七牛云存储的图片名称
            data.append({
                'id':bk.book_id,
                'imgURL':'http://{}/{}'.format(current_app.config['QINIU_SETTINGS']['host'],bk.cover),
                'title':bk.book_name
            })
        db.session.commit()
        return jsonify(data)
    # 如果书架中有书籍数据，遍历书籍数据，获取每本书的数据
    else:
        for bk in mybooks:
            data.append({
                'id':bk.book_id,
                'imgURL':'http://{}/{}'.format(current_app.config['QINIU_SETTINGS']['host'],bk.cover),
                'title':bk.book_name
            })
        # 4.返回书籍数据
        return jsonify(data)

# 定义路由，书架管理--添加书籍
@login_required
@mybooks_bp.route("/<book_id>",methods=['POST'])
def add_book(book_id):
    """
    book_id：url固定参数，必须作为视图参数直接传入，Flask中使用转换器进行处理，默认的数据类型是str；
    :return:
    """
    # 1.添加登录验证装饰器
    user_id = g.user_id
    # 2.接收参数，书籍id
    # 3.根据书籍id，查询书籍表，确认数据的存在
    book = Book.query.filter(Book.book_id==book_id).first()
    # 确认查询结果
    if not book:
        return jsonify(msg='书籍不存在'),404
    # 4.查询书架表，确认该书在书架中是否存在
    book_shelf = BookShelf.query.filter(BookShelf.user_id==user_id,BookShelf.book_id==book_id).first()
    # 判断书架的查询结果
    if not book_shelf:
        # 5.如果书架中不存在，添加书籍
        bk_shelf = BookShelf(
            user_id=user_id,
            book_id=book.book_id,
            book_name=book.book_name,
            cover=book.cover
        )
        db.session.add(bk_shelf)
        db.session.commit()
        # 返回添加成功的信息
        return jsonify(msg='添加成功')
    else:# 否则，书架中该书籍已经存在
        return jsonify(msg='书架中该书籍已经存在'),400

# 定义路由，书架管理--删除书籍
@login_required
@mybooks_bp.route("/<book_id>",methods=['DELETE'])
def del_book(book_id):
    # - 1.添加登录验证装饰器
    user_id = g.user_id
    # - 2.接收参数，书籍id
    bk_shelf = BookShelf.query.filter_by(user_id=user_id,book_id=book_id).first()
    # - 3.根据书籍id，查询书籍表，确认数据的存在
    if not bk_shelf:
        return jsonify(msg='该书籍在书架中不存在'),400
    # - 4.删除书籍
    db.session.delete(bk_shelf)
    db.session.commit()
    return jsonify(msg='删除成功')
    pass


# 定义路由，书架管理--最后阅读
@login_required
@mybooks_bp.route("/last")
def book_last_reading():
    # 1.使用登录验证装饰器，获取用户信息
    user_id = g.user_id
    user = User.query.get(user_id)
    read_rate = None
    # 2.判断用户没有阅读书籍
    if not user.last_read:
        # 3.如果用户没有阅读，默认查询第一本书籍，当做用户的阅读书籍
        # -----也可以查询书架的第一本书
        book = Book.query.first()
        # 保存用户的阅读书籍的id
        user.last_read = book.book_id
        # 4.查询该书籍的章节信息，默认升序排序，
        bk_chapter = BookChapters.query.filter_by(book_id=book.book_id).order_by(BookChapters.chapter_id.asc()).first()
        # 保存用户的阅读书籍的章节信息
        user.last_read_chapter_id = bk_chapter.chapter_id
        # - 把查询结果，存入阅读进度表
        read_rate = ReadRate(
            user_id=user.id,
            book_id=book.book_id,
            chapter_id=bk_chapter.chapter_id,
            chapter_name=bk_chapter.chapter_name
        )
        # 保存数据
        db.session.add(read_rate)
        db.session.add(user)
        # 保存两个对象，参数必须列表
        # db.session.add_all([read_rate,user])
        db.session.commit()
    # 5.如果用户阅读书籍，查询用户阅读的书籍
    else:
        book = Book.query.get(user.last_read)
    # 6.判断是否有阅读进度，如果没有，查询阅读进度表
    if not read_rate:
        read_rate = ReadRate.query.filter_by(
            user_id=user.id,
            book_id=book.book_id,
            chapter_id=user.last_read_chapter_id
        ).first()
    # 7.返回查询结果
    data = {
        'id':book.book_id,
        'title':book.book_name,
        'chapter':read_rate.chapter_name,
        'progress':read_rate.rate,
        'imgURL':'http://{}/{}'.format(current_app.config['QINIU_SETTINGS']['host'],book.cover)
    }
    # 转成json格式返回数据
    return jsonify(data)
    pass
