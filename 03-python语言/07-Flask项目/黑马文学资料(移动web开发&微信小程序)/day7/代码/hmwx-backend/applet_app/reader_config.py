# 导入蓝图
from flask import Blueprint,request,jsonify,g

# 导入用户模型类
from models import User,db
# 导入登录验证装饰器
from lib.decoraters import login_required
# 创建蓝图对象
config_bp = Blueprint('config',__name__,url_prefix='/config')

# 定义路由，用户阅读偏好设置
@login_required
@config_bp.route("/preference",methods=['POST'])
def preference():
    # 1.获取参数，post请求体中json数据
    gender = request.json.get('gender')
    gender = int(gender)
    # 2.校验参数，性别的范围
    if gender not in [0,1]:
        return jsonify(msg='性别参数错误')
    # 3.查询数据库，用户表，获取用户信息
    # User.query.filter_by(user_id=g.user_id).update({'gender':gender})
    # db.session.commit()
    user = User.query.filter_by(id=g.user_id).first()
    user.gender = gender
    # 4.保存数据、提交数据
    db.session.add(user)
    db.session.commit()
    # 5.返回结果
    return jsonify(msg='设置成功')


# 定义路由，用户阅读器设置
@login_required
@config_bp.route('/reader',methods=['POST'])
def reader_config():
    # 1.获取参数、亮度、字号、背景、翻页效果
    brightness = request.json.get('brightness')
    font_size = request.json.get('font_size')
    background = request.json.get("background")
    turn = request.json.get('turn')
    # 2.查询数据库，用户表，根据用户id查询用户信息
    user = User.query.get(g.user_id)
    # 3.保存设置信息，提交数据
    if brightness:
        user.brightness = brightness
    if font_size:
        user.fontSize = font_size
    if background:
        user.background = background
    if turn:
        user.turn = turn
    db.session.add(user)
    db.session.commit()
    # 4.返回结果
    return jsonify(msg='设置成功')