from django import http
from django.contrib.auth import login, logout, authenticate

from django.db import DatabaseError, DataError
from django.http import request
from django.shortcuts import render, redirect
import re, sys, json, logging
# print(sys.path)
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django_redis import get_redis_connection

from carts.utils import merge_cart_cookie_to_redis
from users.models import User
from meiduo_mall.utils.response_code import RETCODE
from meiduo_mall.utils.views import LoginRequiredJsonMixin
from celery_tasks.email.tasks import send_verify_email
from users.utils import generate_verify_email_url, check_verify_email_token
from .models import Address
from . import constants
from goods.models import SKU

logger = logging.getLogger('django')

class UserBrowseHistory(LoginRequiredJsonMixin, View):
    def post(self, request):
        # 保存用户浏览记录
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        # 校验参数
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return http.HttpResponseForbidden('sku_id不正确')
        # 保存数据到redis
        redis_conn = get_redis_connection('history')
        user = request.user
        pl = redis_conn.pipeline()
        # 去重
        pl.lrem('history_%s' % user.id, 0, sku_id)
        # 添加
        pl.lpush('history_%s' % user.id, sku_id)
        # 截取
        pl.ltrim('history_%s' % user.id, 0, 4)
        pl.execute()
        # 返回响应
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})

    def get(self, request):
        # 查询浏览记录
        # {
        #     "code": "0",
        #     "errmsg": "OK",
        #     "skus": [
        #         {
        #             "id": 6,
        #             "name": "Apple iPhone 8 Plus (A1864) 256GB 深空灰色 移动联通电信4G手机",
        #             "default_image_url": "http://image.meiduo.site:8888/group1/M00/00/02/CtM3BVrRbI2ARekNAAFZsBqChgk3141998",
        #             "price": "7988.00"
        #         },
        #         ......
        #     ]
        # }
        user = request.user
        redis_conn = get_redis_connection('history')
        sku_ids = redis_conn.lrange('history_%s' % user.id, 0, -1)
        skus = []
        for sku_id in sku_ids:
            sku = SKU.objects.get(id=sku_id)
            skus.append({
                'id': sku.id,
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': sku.price
            })

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'skus': skus})


class ChangePasswordView(LoginRequiredMixin, View):
    """修改密码"""

    def get(self, request):
        return render(request, 'user_center_pass.html')

    def post(self, request):
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')
        if not all([old_password, new_password, new_password2]):
            return http.HttpResponseForbidden('缺少必传参数')
        try:
            request.user.check_password(old_password)
        except Exception as e:
            logger.error(e)
            return render(request, 'user_center_pass.html', {'origin_pwd_errmsg': '原始密码错误'})
        if not re.match(r'^[0-9A-Za-z]{8,20}$', new_password):
            return http.HttpResponseForbidden('密码最少8位，最长20位')
        if new_password != new_password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        try:
            request.user.set_password(new_password)
            request.user.save()
        except Exception as e:
            logger.error(e)
            return render(request, 'user_center_pass.html', {'change_pwd_errmsg': '修改密码失败'})
        logout(request)
        response = redirect(reverse('user:login'))
        response.delete_cookie('username')
        return response


class DefaultAddressView(LoginRequiredJsonMixin, View):
    """设置默认地址"""

    def put(self, request, address_id):
        try:
            # 接收参数,查询地址
            address = Address.objects.get(id=address_id)
            request.user.default_address = address
            request.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '设置默认地址失败'})

        # 响应设置默认地址结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '设置默认地址成功'})


class UpdateTitleAddressView(LoginRequiredJsonMixin, View):
    def put(self, request, address_id):
        json_dict = json.loads(request.body.decode())
        title = json_dict.get('title')
        try:
            address = Address.objects.get(id=address_id)
            address.title = title
            address.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '设置标题失败'})
        # 响应删除地址结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '设置标题成功'})


class UpdateDestroyAddressView(LoginRequiredJsonMixin, View):
    def put(self, request, address_id):
        json_dict = json.loads(request.body.decode())

        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return http.HttpResponseForbidden('缺少参数')
        if not re.match('^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('mobile有误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return http.HttpResponseForbidden('参数tel有误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return http.HttpResponseForbidden('参数email有误')

        # 保存地址信息
        try:
            # 返回的是收影响的行数
            Address.objects.filter(id=address_id).update(
                user=request.user,
                title=receiver,  # 标题默认就是收货人
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email,
            )
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '修改地址失败'})
        try:
            address = Address.objects.get(id=address_id)
            address_dict = {
                'id': address.id,
                'title': address.title,  # 标题默认就是收货人
                'receiver': address.receiver,
                'province': address.province.name,
                'city': address.city.name,
                'district': address.district.name,
                'place': address.place,
                'mobile': address.mobile,
                'tel': address.tel,
                'email': address.email,
            }
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '修改地址失败'})
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '修改地址成功', 'address': address_dict})

    def delete(self, request, address_id):
        try:
            address = Address.objects.get(id=address_id)
            address.is_deleted = True
            address.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '删除地址失败'})
        # 响应删除地址结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '删除地址成功'})


class CreateAddressView(LoginRequiredJsonMixin, View):
    """新增地址"""

    def post(self, request):
        json_dict = json.loads(request.body.decode())

        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return http.HttpResponseForbidden('缺少参数')
        if not re.match('^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('mobile有误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return http.HttpResponseForbidden('参数tel有误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return http.HttpResponseForbidden('参数email有误')

        count = Address.objects.filter(user=request.user, is_deleted=False).count()
        # count = request.user.addresses.count()
        if count >= constants.USER_ADDRESS_COUNTS_LIMIT:
            return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '超过地址数量上限'})

        # 保存地址信息
        try:
            address = Address.objects.create(
                user=request.user,
                title=receiver,  # 标题默认就是收货人
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email,
            )
            # 设置默认地址
            if request.user.default_address is None:
                request.user.default_address = address
                request.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '新增地址失败'})
        address_dict = {
            'id': address.id,
            'title': address.title,  # 标题默认就是收货人
            'receiver': address.receiver,
            'province': address.province.name,
            'city': address.city.name,
            'district': address.district.name,
            'place': address.place,
            'mobile': address.mobile,
            'tel': address.tel,
            'email': address.email,
        }
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '新增地址成功', 'address': address_dict})


class AddressView(LoginRequiredMixin, View):
    # 用户收货地址
    def get(self, request):
        addresses = Address.objects.filter(user=request.user, is_deleted=False)
        address_dict_list = []
        for address in addresses:
            address_dict = {
                'id': address.id,
                'title': address.title,
                'receiver': address.receiver,
                'province': address.province.name,
                'city': address.city.name,
                'district': address.district.name,
                'place': address.place,
                'mobile': address.mobile,
                'tel': address.tel,
                'email': address.email,
            }
            address_dict_list.append(address_dict)
        context = {
            'default_address_id': request.user.default_address_id,
            'addresses': address_dict_list

        }
        return render(request, 'user_center_site.html', context=context)


class VerifyEmailView(View):
    """验证邮箱"""

    def get(self, request):
        token = request.GET.get('token')
        if not token:
            return http.HttpResponseBadRequest('缺少token')
        user = check_verify_email_token(token)
        if not user:
            return http.HttpResponseForbidden('无效的token')
        try:
            user.email_active = True
            user.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('激活失败')
        return redirect(reverse('users:info'))


class EmailView(LoginRequiredJsonMixin, View):
    """添加邮箱"""

    def put(self, request):
        # 更新、修改
        json_str = request.body.decode()
        json_dict = json.loads(json_str)
        email = json_dict.get('email')
        if email is None:
            return http.HttpResponseForbidden('缺少必传参数')
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.HttpResponseForbidden('参数有误')
        # 保存到数据库
        try:
            # User.object.create(email=email)
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '邮箱格保存失败'})
        # 异步发送邮件
        verify_url = generate_verify_email_url(request.user)  # request.user 当前登录用户
        send_verify_email.delay(email, verify_url)  # email 收件人邮箱
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '邮箱格保存成功'})


class UserInfoView(LoginRequiredMixin, View):
    # login_url = '/login/'
    # redirect_field_name = 'redirect_to'
    # http: // 127.0.0.1: 8000 / login /?next =/ info /
    def get(self, request):
        context = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active,
        }
        return render(request, 'user_center_info.html', context=context)


# 退出视图
class LogoutView(View):
    def get(self, request):
        logout(request)
        response = redirect(reverse('contents:index'))
        response.delete_cookie('username')
        return response


# 登录视图
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')

        if not all([username, password]):
            return http.HttpResponseForbidden('缺少必传参数')  # 403只用于校验参数
        if not re.match(r'^[0-9a-zA-Z-_]{5,20}$', username):
            return http.HttpResponseForbidden('请输入正确的用户名或手机号')
        if not re.match(r'^[0-9a-zA-Z]{8,20}$', password):
            return http.HttpResponseForbidden('密码最少8位，最长20位')
        # #认证用户：使用账号查询用户是否存在，如果用户存在，再校验密码是否正确
        # user = User.objects.get(username=username)
        # user.check_password()  django认证系统帮我们封装好了
        user = authenticate(username=username, password=password)
        if user is None:
            # 表单提交所以不是局部刷新
            return render(request, 'login.html', {'account_errmsg': "用户名或密码错误"})
        # 状态保持
        login(request, user)
        if remembered != 'on':
            # 没有记住用户：浏览器会话结束就过期
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(None)
        # http: // 127.0.0.1: 8000 / login /?next =/ info /
        next_url = request.GET.get('next')
        if next_url:
            response = redirect(next_url)
        else:
            response = redirect(reverse('contents:index'))
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)
        response = merge_cart_cookie_to_redis(request=request, user=user, response=response)
        # 用户登陆
        return response


# 用户名重复
class UsernameCountView(View):
    def get(self, request, username):
        """
        :param username: 用户名
        :return: json
        """
        # 接受参数 username
        # 校验参数 username
        # 查询数据库count
        count = User.objects.filter(username=username).count()
        # 返回响应
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'count': count})


# 手机号重复
class MobileCountView(View):
    def get(self, request, mobile):
        """
        :param mobile: 手机号
        :return: json
        """
        # 查询数据库count
        count = User.objects.filter(mobile=mobile).count()
        # 返回响应
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'count': count})


# 注册视图
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 1.接受参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        sms_code_cli = request.POST.get('sms_code')
        allow = request.POST.get('allow')
        # 2.校验参数,前后端校验要分开
        # 判断参数是否齐全
        if not all([username, password, password2, mobile, allow]):
            return http.HttpResponseForbidden('参数不齐，注册失败')
        # 判断用户名是否是5-20个字符
        if not re.match(r'^[0-9a-zA-Z_-]{5,20}$', username):
            return http.HttpResponseForbidden('请输入5-20个字符的用户名')
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9a-zA-Z]{8,20}$', password):
            return http.HttpResponseForbidden('请输入8-20个数字的密码')
        # 判断两次密码是否一致
        if password != password2:
            return http.HttpResponseForbidden('两次密码输入不一样')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('手机号不合法')
        # 判断是否勾选用户协议
        if allow != 'on':
            return http.HttpResponseForbidden('没有勾选用户协议')
        # 判断短信验证是否正确
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_code_%s' % mobile)
        if sms_code_server is None:
            return render(request, 'register.html', {'sms_code_errmsg': '短信验证码过期'})
        if sms_code_server.decode() != sms_code_cli:
            return render(request, 'register.html', {'sms_code_errmsg': '短信验证码错误'})

        # 3.保存数据(用户注册的核心)
        # save_data={
        #     'username': username,
        #     'password': password,
        #     'mobile': mobile,
        # }
        # try:
        #      User.objects.create_user(**save_data)
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '注册失败'})
        # 状态保持
        login(request, user)
        # 4.返回响应返回首页
        response = redirect(reverse('contents:index'))

        # 登录时用户名写入到cookie，有效期15天
        response.set_cookie('username', user.username, max_age=3600 * 24 * 15)

        return response
