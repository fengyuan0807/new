import os

from alipay import AliPay
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django import http
from django.conf import settings

# Create your views here.
from meiduo_mall.utils.response_code import RETCODE
from orders.models import OrderInfo
from .models import Payment


class PaymentStatusView(LoginRequiredMixin, View):
    def get(self, request):
        query_dict = request.GET
        data = query_dict.dict()
        signature = data.pop('sign')

        # 创建支付宝支付对象
        alipy = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "keys/app_private_key.pem"),
            alipay_public_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                "keys/alipay_public_key.pem"),
            sign_type="RSA2",
            debug=settings.ALIPAY_DEBUG
        )
        success = alipy.verify(data, signature)
        # 校验这个重定向是否是alipay重定向过来的
        if success:
            trade_id = data.get('trade_no')  # 支付宝交易号
            order_id = data.get('out_trade_no')  # 商户订单号
            Payment.objects.create(
                order_id=order_id,
                trade_id=trade_id
            )
            OrderInfo.objects.filter(order_id=order_id, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID']).update(
                status=OrderInfo.ORDER_STATUS_ENUM['UNCOMMENT']
            )
            context = {
                'trade_id':trade_id
            }
            return render(request, 'pay_success.html', context)
        else:
            return http.HttpResponseForbidden('非法访问')

class PaymentView(LoginRequiredMixin, View):
    """对接支付宝接口"""

    def get(self, request, order_id):
        user = request.user
        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user,
                                          status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'])
        except OrderInfo.DoesNotExist:
            return http.HttpResponseForbidden('订单信息错误')

        # 创建支付宝支付对象
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调url
            app_private_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                              "keys/app_private_key.pem"),
            alipay_public_key_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                "keys/alipay_public_key.pem"),
            sign_type="RSA2",
            debug=settings.ALIPAY_DEBUG
        )

        # 生成登录支付宝连接
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount),
            subject="美多商城%s" % order_id,
            return_url=settings.ALIPAY_RETURN_URL,
        )

        # 响应登录支付宝连接
        # 真实环境电脑网站支付网关：https://openapi.alipay.com/gateway.do? + order_string
        # 沙箱环境电脑网站支付网关：https://openapi.alipaydev.com/gateway.do? + order_string
        alipay_url = settings.ALIPAY_URL + "?" + order_string
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'alipay_url': alipay_url})
