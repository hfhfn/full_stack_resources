# 导入蓝图
from flask import Blueprint,request,jsonify

# 导入模型类
from models import SearchKeyWord

# 创建蓝图对象
search_bp = Blueprint('search',__name__,url_prefix='/search')


# 定义路由，关键词热门搜索
@search_bp.route("/tags")
def tag_list():
    # 1.获取参数，用户搜索的关键词key_word
    key_word = request.args.get("key_word")
    # 校验参数
    if not key_word:
        return jsonify([])
    # 2.根据参数，查询数据库，搜索关键词表进行过滤查询、过滤关键词
    # 热门搜索词，默认提供10条数据
    search_list = SearchKeyWord.query.filter(SearchKeyWord.keyword.contains(key_word)).limit(10)
    # 3.返回查询结果
    data = [{
        'title':index.keyword,
        'isHot':index.is_hot,
    }for index in search_list]
    # 转成json返回
    return jsonify(data)

