from django import http
from django.shortcuts import render
import random, logging
from django.views import View
from django_redis import get_redis_connection
from celery_tasks.sms.tasks import send_sms_code
from verifications.libs.captcha.captcha import captcha
from verifications import constants
from meiduo_mall.utils.response_code import RETCODE
from verifications.libs.yuntongxun.ccp_sms import CCP

# Create your views here.
logger = logging.getLogger('django')


# 短信验证码
class SMSCodeView(View):
    def get(self, request, mobile):
        # 获取数据 mobile,image_code,uuid
        image_code_cli = request.GET.get('image_code')
        uuid = request.GET.get('uuid')
        # 校验数据
        if not all([image_code_cli, uuid]):
            return http.HttpResponseForbidden('缺少必传参数')

        redis_conn = get_redis_connection('verify_code')
        # 判断用户是否频繁发送短信验证码
        # 提取发送短信验证码的标记
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return http.JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '发送短信过于频繁'})
        # 提取图形验证码
        image_code_server = redis_conn.get('img_%s' % uuid)

        if image_code_server is None:
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图形验证码已经失效'})
        # 删除图形验证码
        redis_conn.delete('img_%s' % uuid)
        # 对比图形验证码
        image_code_cli = image_code_cli.encode()
        if image_code_server.lower() != image_code_cli.lower():
            return http.JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '输入图形验证错误'})

        # 生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info('短信验证码：%s' % sms_code)  # 手动输出日志

        # 1.创建Redis管道
        p1 = redis_conn.pipeline()
        # 2.将Redis请求添加到队列
        p1.setex('sms_code_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        p1.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        # 3.执行请求
        p1.execute()
        # 保存短信验证码
        # redis_conn.setex('sms_code_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 保存发送短信验证码的标记
        # redis_conn.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)


        # # 发送短信验证码
        # ccp = CCP()
        # ccp.send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60],
        #                       constants.SEND_SMS_TEMPLATE_ID)
        # Celery异步发送短信验证码

        send_sms_code.delay(mobile, sms_code)
        # 响应数据
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '短信发送成功'})


# 获取图形验证码
class ImageCodeView(View):
    def get(self, request, uuid):
        """
        :param request: 请求对象
        :param uuid:唯一标识图形验证码所属与的用户
        :return: image/jpg
        """
        # 接受参数
        # 提取参数
        # 校验参数
        # 生成图形验证码
        text, image = captcha.generate_captcha()
        # 保存图形验证码,文字保存在redis
        redis_conn = get_redis_connection('verify_code')
        redis_conn.setex('img_%s' % uuid, constants.IMAGE_CODE_REDIS_EXPIRES, text)
        logger.info('图形验证码：%s' % text)
        # 响应图形验证（图片）
        # HttpResponse(content=响应体, 表示返回的内容, content_type=响应体数据类型, status=状态码)
        return http.HttpResponse(image, content_type='image/jpg')
