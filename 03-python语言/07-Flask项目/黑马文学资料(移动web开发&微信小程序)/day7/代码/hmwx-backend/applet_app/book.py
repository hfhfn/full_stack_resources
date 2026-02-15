# 导入蓝图
from flask import Blueprint,request,jsonify,g,current_app
# 导入日期模块
from datetime import datetime

# 导入模型类
from models import Book,BookChapters,BookChapterContent,ReadRate,BrowseHistory,db
# 创建蓝图对象
book_bp = Blueprint('book',__name__,url_prefix='/book')

# 定义路由,小说目录列表
@book_bp.route('/chapters/<int:book_id>')
def chapter_list(book_id):
    # 1.获取查询字符串参数，page/pagesize/order
    page = request.args.get('page',1,int)
    pagesize = request.args.get('pagesize',10,int)
    order = request.args.get("order",0,int)
    # 2.根据书籍id参数，查询书籍表
    book = Book.query.get(book_id)
    if not book:
        return jsonify(msg='书籍不存在'),404
    # 3.查询书籍章节目录表，按照书籍id进行过滤查询
    query = BookChapters.query.filter(BookChapters.book_id==book_id)
    # 4.根据order参数的排序条件，如果1倒序排序，如果0升序排序
    if order == 1:
        query = query.order_by(BookChapters.chapter_id.desc())
    else:
        query = query.order_by(BookChapters.chapter_id.asc())
    # 5.对排序的结果，进行分页处理
    paginate = query.paginate(page,pagesize,False)
    data_list = paginate.items
    # 6.遍历分页的数据，获取章节信息
    items = []
    for data in data_list:
        items.append({
            'id':data.chapter_id,
            'title':data.chapter_name
        })
    # 构造响应数据
    chapter_data = {
        'counts':paginate.total,
        'pages':paginate.pages,
        'page':paginate.page,
        'items':items
    }
    # 7.转成json格式，返回数据
    return jsonify(chapter_data)


# 定义路由，小说阅读
@book_bp.route("/reader/<int:book_id>")
def reader_book(book_id):
    # 1.根据书籍id，查询书籍表，确认书籍的存在
    book = Book.query.get(book_id)
    if not book:
        return jsonify(msg='书籍不存在'),404
    # 2.获取查询字符串参数章节id，校验参数
    chapter_id = request.args.get('chapter_id',-1,int)
    if chapter_id < 1:
        return jsonify(msg='章节id不能小于1'),400
    # 3.根据章节id，查询书籍章节表
    chapter = BookChapters.query.get(chapter_id)
    # 4.判断查询结果
    if not chapter:
        return jsonify(msg='章节不存在'),404
    # 5.如果数据存在，查询书籍内容表
    content = BookChapterContent.query.filter_by(book_id=book_id,chapter_id=chapter_id).first()
    # 6.如果用户登录，查询用户阅读进度表；
    progress = None
    if g.user_id:
        progress = ReadRate.query.filter_by(book_id=book_id,chapter_id=chapter_id,user_id=g.user_id).first()
    # 构造响应数据
    data = {
        'id':book_id,
        'title':book.book_name,
        'chapter_id':chapter.chapter_id,
        'chapter_name':chapter.chapter_name,
        'progress':progress.rate if progress else 0,
        'article_content':content.content if content else ''
    }
    # 7.返回
    return jsonify(data)


# 定义路由，小说详情
@book_bp.route('/<book_id>')
def book_detail(book_id):
    # 1.根据书籍id，查询数据书籍表
    book = Book.query.get(book_id)
    if not book:
        return jsonify(msg='书籍不存在'),404
    # 2.判断，如果用户登录，查询用户的浏览记录
    # 查询过滤条件，必须加上书籍id，一个用户可以阅读多本书
    if g.user_id:
        bs_data = BrowseHistory.query.filter_by(user_id=g.user_id,book_id=book_id).first()
        # 3.判断查询结果，保存数据，浏览记录的时间
        if not bs_data:
            bs_data = BrowseHistory(user_id=g.user_id,book_id=book_id)
        bs_data.updated = datetime.now()
        db.session.add(bs_data)
        db.session.commit()
    # 4.如果用户未登录，根据书籍id查询书籍章节表，默认倒序排序。
    chapter = BookChapters.query.filter_by(book_id=book_id).order_by(BookChapters.chapter_id.desc()).first()
    # 5.返回结果
    data = {
        'id':book.book_id,
        'title':book.book_name,
        'intro':book.intro,
        'author':book.author_name,
        'status':book.status,
        'category_id':book.cate_id,
        'category_name':book.cate_name,
        'words':book.word_count,
        'imgURL':'http://{}/{}'.format(current_app.config['QINIU_SETTINGS']['host'],book.cover),
        'lastChapter':chapter.chapter_name if chapter else None
    }
    return jsonify(data)

