from django.conf import settings
from itsdangerous import BadData
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import constants


def check_access_token(access_token_openid):
    # 返回秘文
    s = Serializer(settings.SECRET_KEY, constants.ACCESS_TOKEN_EXPIRES)
    try:
        data = s.loads(access_token_openid)
    except BadData:
        return None
    else:
        return data.get('openid')


def generate_access_token(openid):
    # 返回秘文
    s = Serializer(settings.SECRET_KEY, constants.ACCESS_TOKEN_EXPIRES)
    data = {'openid': openid}
    # dumps 将字典转换成二进制(b'adsadafa')
    token = s.dumps(data).decode()
    return token
