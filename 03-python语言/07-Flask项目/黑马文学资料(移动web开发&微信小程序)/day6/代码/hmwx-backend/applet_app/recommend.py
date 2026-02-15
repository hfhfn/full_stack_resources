# 导入蓝图
from flask import Blueprint,current_app,jsonify

# 导入模型类
from models import BookBigCategory,Book

# 创建蓝图对象
recommend_bp = Blueprint('recommend',__name__,url_prefix='/recommend')


# 定义路由，推荐--同类热门数据推荐
@recommend_bp.route("/hots/<int:category_id>")
def recommends(category_id):
    # 1.定义路由，接收url路径参数，作为视图函数的参数
    # 2.根据参数分类id，查询数据库、获取大分类数据
    big_category = BookBigCategory.query.get(category_id)
    # 定义列表容器，用来存储最终要返回的书籍数据
    books= []
    # 3.判断如果有大分类数据
    if big_category:
        # 4.获取该大分类下面的二级分类数据
        # seconds_ids = []
        # for i in big_category.second_cates:
        #     seconds_ids.append(i.cate_id)
        seconds_id = [i.cate_id for i in big_category.second_cates]
        # 5.根据分类，查询书籍表，获取对应分类的书籍数据，默认查询4条
        book_list = Book.query.filter(Book.cate_id.in_(seconds_id)).limit(4)
        # 6.保存书籍的基本信息
        for book in book_list:
            books.append({
                'id':book.book_id,
                'title':book.book_name,
                'intro':book.intro,
                'author':book.author_name,
                'state':book.status,
                'category_id':book.cate_id,
                'category_name':book.cate_name,
                'imgURL':'http://{}/{}'.format(current_app.config['QINIU_SETTINGS']['host'],book.cover)
            })
    else:
        # 7.如果没有大分类数据，默认返回4条数据。
        book_list = Book.query.limit(4)
        for book in book_list:
            books.append({
                'id': book.book_id,
                'title': book.book_name,
                'intro': book.intro,
                'author': book.author_name,
                'state': book.status,
                'category_id': book.cate_id,
                'category_name': book.cate_name,
                'imgURL': 'http://{}/{}'.format(current_app.config['QINIU_SETTINGS']['host'], book.cover)
            })
    # 转成json格式，返回书籍列表
    return jsonify(books)


