# Flask基本程序实现
from flask import Blueprint,request,jsonify,current_app
# 导入日期模块
from datetime import datetime,timedelta

# 导入微信工具
from lib.wxauth import get_wxapp_session_key,get_user_info
# 导入模型类
from models.user import User
# 导入数据库sqlalchemy对象
from models import db
# 导入jwt工具
from lib.jwt_utils import generate_jwt


# 创建蓝图对象
user_bp = Blueprint('user_bp',__name__,url_prefix='/users')
# 定义蓝图路由
# @user_bp.route('/')
# def user_info():
#     return 'user info'

# app.register_blueprint(user_bp)

def _generate_jwt_token(user_id):
    # 参数：user_id表示生成token的载荷中存储用户信息
    # 步骤：
    # 1、生成当前时间
    now = datetime.utcnow()
    # 2、根据时间差，指定token的过期时间,
    # expire = now + timedelta(hours=24)
    expiry = now + timedelta(hours=current_app.config.get("JWT_EXPIRE_TIME"))
    # 3、调用jwt工具，传入过期时间
    token = generate_jwt({'user_id':user_id},expire=expiry)
    # 4、返回token
    return token
    pass

@user_bp.route("/login",methods=['POST'])
def login():
    #- 1、获取参数code,用户登录凭证，有效期五分钟
    code = request.json.get('code','')
    #- 2、获取参数iv、envryptedData
    iv = request.json.get('iv','')
    envryptedData = request.json.get('envryptedData','')
    # 判断参数是否存在
    if not iv or not envryptedData or not code:
        return jsonify(msg='参数错误'),403
    #- 3、调用微信工具，获取session_key
    data = get_wxapp_session_key(code)
    if 'session_key' not in data:
        return jsonify(msg='获取session_key信息失败',data=data),500
    #- 4、根据session_key，调用微信工具，获取用户信息
    session_key = data['session_key']
    user_info = get_user_info(envryptedData,iv,session_key)
    #- 5、判断是否获取到openID
    if 'openId' not in user_info:
        return jsonify(msg='获取用户信息失败',user_info=user_info),403
    #- 6、保存用户数据
    #- 查询mysql数据库，判断openID是否存在
    openid = user_info['openId']
    # User.query.filter(User.openId==openid).first()
    user = User.query.filter_by(openId=openid).first()
    if not user:
        user = User(user_info)
        db.session.add(user)
        # flush表示把当前的模型类对象，刷到数据库中
        db.session.flush()
    #- 如果用户存在，更新用户信息
    else:
        user.update_info(user_info)
        db.session.commit()
    # - 7、调用jwt工具，生成token
    token = _generate_jwt_token(user.id)
    # - 8、返回数据
    ret_data = {
        'token':token,
        'user_info':{
            'uid':user.id,
            'gender':user.gender,
            'avatarUrl':user.avatarUrl
        },
        "config": {
            "preference": user.preference,
            "brightness": user.brightness,
            "fontSize": user.fontSize,
            "background": user.background,
            "turn": user.turn
        }
    }
    return jsonify(ret_data)
    pass