import requests
from .WXBizDataCrypt import WXBizDataCrypt

WXAPP_ID = 'wxdab2c9193cb7e2a9'

WXAPP_SECRET = '66ebd51238192cb95dfc82c4cdff034f'


def get_wxapp_session_key(code):
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % (
    WXAPP_ID, WXAPP_SECRET, code)
    data = requests.get(url).json()
    print(data)
    return data


def get_user_info(encryptedData, iv, session_key):
    pc = WXBizDataCrypt(WXAPP_ID, session_key)
    return pc.decrypt(encryptedData, iv)