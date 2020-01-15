from django.conf import settings
from django import http
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View

from carts.utils import merge_cart_cookie_to_redis
from meiduo_mall.utils.response_code import RETCODE
from oauth.models import OAuthQQUser
from QQLoginTool.QQtool import OAuthQQ
import logging, re
from django_redis import get_redis_connection
from oauth.utils import generate_access_token, check_access_token
from users.models import User
from django.db import DatabaseError

logger = logging.getLogger('django')


# Create your views here.
class QQAuthUserView(View):
    # 处理qq回调视图
    def get(self, request):
        code = request.GET.get('code')
        if not code:
            return http.HttpResponseForbidden('缺少code')
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)  # state只需要携带一次
        try:
            access_token = oauth.get_access_token(code)
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('OAuth2.0认证失败')
        try:
            # 查询是否绑定
            oauth_qq_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 如果openid没绑定美多商城用户
            # 加密的openid
            access_token_openid = generate_access_token(openid)
            context = {'access_token_openid': access_token_openid}
            # oauth_callback.html绑定用户的界面
            return render(request, 'oauth_callback.html', context)
        else:
            # 如果openid已绑定美多商城用户
            login(request, oauth_qq_user.user)
            # 哪里点击的qq登录回哪里
            next_url = request.GET.get('state')
            response = redirect(next_url)
            response.set_cookie('username', oauth_qq_user.user.username, max_age=3600 * 24 * 15)
            response = merge_cart_cookie_to_redis(request=request, user=oauth_qq_user.user, response=response)
            return response

    def post(self, request):
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        sms_code_client = request.POST.get('sms_code')
        access_token_openid = request.POST.get('access_token_openid')
        if not all([mobile, password, sms_code_client]):
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('手机号码格式错误')
        if not re.match(r'^[0-9a-zA-Z]{8,20}$', password):
            return http.HttpResponseForbidden('密码最少8位，最长20位')

        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_code_%s' % mobile)
        if sms_code_server is None:
            # oauth_callback.html绑定用户的界面
            return render(request, 'oauth_callback.html', {'sms_code_errmsg': '短信验证码过期'})
        if sms_code_server.decode() != sms_code_client:
            return render(request, 'oauth_callback.html', {'sms_code_errmsg': '短信验证码错误'})
        # 判断openid是否有效，错误提示放在sms——code-errmag
        openid = check_access_token(access_token_openid)
        if not openid:
            return render(request, 'oauth_callback.html', {'openid_errmsg': '无效的openid'})
        try:
            # 使用手机号查询用户是否存在
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 用户不存在,新建用户
            user = User.objects.create_user(username=mobile, password=password, mobile=mobile)
        else:
            # 如果用户存在,检查用户密码
            if not user.check_password(password):
                return render(request, 'oauth_callback.html', {'account_errmsg': '用户名或密码错误'})
        # 将用户绑定openid
        try:
            # oauth_qq_user =OAuthQQUser(user=user, openid=openid)
            # oauth_qq_user.save()
            oauth_qq_user = OAuthQQUser.objects.create(user=user, openid=openid)
        except DatabaseError:
            return render(request, 'oauth_callback.html', {'qq_login_errmsg': 'qq登录失败'})
            # 实现状态保持
        login(request, oauth_qq_user.user)
        # 响应绑定结果
        next_url = request.GET.get('state')
        response = redirect(next_url)
        # 登录时用户名写入到cookie，有效期15天
        response.set_cookie(username=oauth_qq_user.user.username,max_age=3600 * 24 * 15)
        response = merge_cart_cookie_to_redis(request=request, user=user, response=response)
        return response


class QQAuthURLView(View):
    # 提供登陆qq登陆界面
    def get(self, request):
        next_url = request.GET.get('next')
        # next_url表示从哪个页面进入到的登录页面，将来登录成功后，就自动回到那个页面
        # 创建工具对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI, state=next_url)
        # 生成qq登陆扫码链接地址
        login_url = oauth.get_qq_url()

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'login_url': login_url})


