from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.conf import settings
from users.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
from users import constants
from itsdangerous import BadData
import logging

logger = logging.getLogger('django')

def check_verify_email_token(token):
    s = serializer(settings.SECRET_KEY, expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)
    try:
        data = s.loads(token)
    except BadData:
        return None
    else:
        user_id = data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
        else:
            return user

def generate_verify_email_url(user):
    s = serializer(settings.SECRET_KEY, expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)
    data = {'user_id': user.id}
    token = s.dumps(data).decode()
    verify_url = settings.EMAIL_VERIFY_URL + '?token=' + token
    return verify_url


def get_user_by_account(account):
    #
    # try:
    #     user = User.objects.get(username=account)
    # except User.DoesNotExist:
    #     try:
    #         user = User.objects.get(mobile=account)
    #     except User.DoesNotExist:
    #         return None
    # return user

    try:
        user = User.objects.filter(Q(username=account) | Q(mobile=account))[0]
    except User.DoesNotExist:
        return None
    return user


class UsernameMobileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        :param request:
        :param username: 用户名或手机号
        :param password:
        :param kwargs:
        :return:
        """
        # 使用账号查询用户
        # 如果可以查询用户，还需要校验密码是否正确
        # 返回user

        user = get_user_by_account(username)
        if user and user.check_password(password):
            return user
        else:
            return None
