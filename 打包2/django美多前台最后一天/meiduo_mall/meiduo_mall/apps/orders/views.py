from decimal import Decimal

from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django_redis import get_redis_connection
from django import http
from django.utils import timezone
from django.db import transaction
from meiduo_mall.utils.views import LoginRequiredJsonMixin

from orders.models import OrderInfo, OrderGoods
from goods.models import SKU, SPU
from users.models import Address

from meiduo_mall.utils.response_code import RETCODE
import json, logging

# Create your views here.
logger = logging.getLogger('django')


class UserOrderInfoView(LoginRequiredMixin, View):
    """订单"""

    def get(self, request, page_num):
        user = request.user
        # 一个用户对应多个订单信息
        orderinfos = OrderInfo.objects.filter(user=user).order_by('-create_time')
        # orders = user.orderinfo_set.all().order_by('-create_time')
        # 遍历所有的订单信息
        for orderinfo in orderinfos:
            # 绑定支付方式
            orderinfo.status_name = OrderInfo.ORDER_STATUS_CHOICES[orderinfo.status - 1][1]
            orderinfo.pay_method_name = OrderInfo.PAY_METHOD_CHOICES[orderinfo.pay_method - 1][1]
            #                         =货到付款PAY_METHOD_CHOICES[0][1]或者是支付宝 [1][1]
            orderinfo.sku_list = []
            orders = orderinfo.skus.all()
            for order in orders:
                sku = order.sku
                sku.count = order.count
                sku.amount = sku.price * sku.count
                orderinfo.sku_list.append(sku)
        page_num = int(page_num)
        try:
            paginator = Paginator(orderinfos, per_page=5)
            page_orders = paginator.page(page_num)
            total_page = paginator.num_pages
        except EmptyPage:
            return http.HttpResponseNotFound('订单不存在')
        context = {
            'page_orders': page_orders,
            'total_page': total_page,
            'page_num': page_num,
        }
        return render(request, 'user_center_order.html', context)


class OrderSuccessView(LoginRequiredMixin, View):
    """订单成功"""

    def get(self, request):
        order_id = request.GET.get('order_id')
        payment_amount = request.GET.get('payment_amount')
        pay_method = request.GET.get('pay_method')

        context = {
            'order_id': order_id,
            'payment_amount': payment_amount,
            'pay_method': pay_method
        }
        return render(request, 'order_success.html', context)


class OrderCommitView(LoginRequiredJsonMixin, View):
    # 订单成功
    def post(self, request):
        json_dict = json.loads(request.body.decode())
        address_id = json_dict.get('address_id')
        pay_method = json_dict.get('pay_method')
        if not all([address_id, pay_method]):
            return http.HttpResponseForbidden('参数不齐全')
        # 判断address_id是否合法
        try:
            address = Address.objects.get(id=address_id)
        except Address.DoseNotExist:
            return http.HttpResponseForbidden('参数address_id错误')
        # 判断pay_method是否合法
        # if pay_method not in [1,2]
        if pay_method not in [OrderInfo.PAY_METHODS_ENUM["CASH"], OrderInfo.PAY_METHODS_ENUM["ALIPAY"]]:
            return http.HttpResponseForbidden('参数pay_method错误')
        # order_id 事件+user_id
        user = request.user
        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)
        # 新建 OrderInfo 数据
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                order = OrderInfo.objects.create(
                    order_id=order_id,
                    user=user,
                    address=address,
                    total_count=0,
                    total_amount=Decimal(0.00),
                    freight=Decimal(10.00),
                    pay_method=pay_method,
                    # status= '待发货'if pay_method=='货到付款' else '待支付'
                    status=OrderInfo.ORDER_STATUS_ENUM["UNSEND"] if pay_method == OrderInfo.PAY_METHODS_ENUM[
                        "CASH"] else
                    OrderInfo.ORDER_STATUS_ENUM["UNPAID"]
                )
                # 从redis中读取购物车数据
                redis_conn = get_redis_connection('carts')
                redis_cart = redis_conn.hgetall('carts_%s' % user.id)  # 字典
                cart_selected = redis_conn.smembers('selected_%s' % user.id)  # 列表[b'sku_id1',b'sku_id2']
                cart = {}
                for sku_id in cart_selected:
                    cart[int(sku_id)] = int(redis_cart[sku_id])
                sku_ids = cart.keys()
                for sku_id in sku_ids:
                    while True:
                        sku = SKU.objects.get(id=sku_id)
                        sku_count = cart[sku.id]
                        sku_amount = sku_count * sku.price
                        if sku_count > sku.stock:
                            transaction.savepoint_rollback(save_id)
                            return http.JsonResponse({'code': RETCODE.STOCKERR, 'errmsg': '库存量不足'})

                        # 乐观锁更新库存和销量
                        origin_stock = sku.stock  # 原始库存
                        new_stock = origin_stock - sku_count
                        origin_sales = sku.sales
                        new_sales = origin_sales + sku_count
                        result = SKU.objects.filter(id=sku_id, stock=origin_stock).update(stock=new_stock,
                                                                                          sales=new_sales)
                        if result == 0:  # 如果等于0 的话 表示有资源抢夺
                            continue
                            # SKU减少库存，增加销量
                        # sku.stock -= sku_count
                        # sku.sales += sku_count
                        # sku.save()
                        sku.spu.sales += sku_count
                        sku.spu.save()
                        OrderGoods.objects.create(
                            order=order,
                            sku=sku,
                            count=sku_count,
                            price=sku.price
                        )
                        # 商品总数
                        order.total_count += sku_count
                        # 商品总金额
                        order.total_amount += sku_amount
                        break
                order.total_amount += order.freight
                order.save()
            except Exception as e:
                logger.error(e)
                transaction.savepoint_rollback(save_id)
                return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '下单失败'})
            transaction.savepoint_commit(save_id)
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'order_id': order_id})


class OrderSettlementView(LoginRequiredMixin, View):
    # 订单页面
    def get(self, request):
        # carts_user_id: {sku_id1: count, sku_id3: count, sku_id5: count, ...}
        # selected_user_id: [sku_id1, sku_id3, ...]
        user = request.user
        try:
            addresses = Address.objects.filter(user=user, is_deleted=False)
        except Address.DoseNotExist:
            addresses = None
        redis_conn = get_redis_connection('carts')
        redis_cart = redis_conn.hgetall('carts_%s' % user.id)  # {b'1':b'20',b'2':b'30',b'3':b'50'}
        cart_selected = redis_conn.smembers('selected_%s' % user.id)  # [b'1,b'2']
        cart = {}  # 构造成{'1':'20'}
        for sku_id in cart_selected:
            cart[int(sku_id)] = int(redis_cart[sku_id])
        sku_ids = cart.keys()
        skus = SKU.objects.filter(id__in=sku_ids)
        total_count = 0
        total_amount = Decimal(0.00)
        #
        for sku in skus:
            sku.count = cart[sku.id]
            sku.amount = sku.price * sku.count
            # 计算总的
            total_count += sku.count
            total_amount += sku.price * sku.count
        freight = Decimal(10.00)
        context = {
            'addresses': addresses,
            'skus': skus,
            'total_count': total_count,
            'total_amount': total_amount,
            'freight': freight,
            'payment_amount': total_amount + freight

        }
        return render(request, 'place_order.html', context=context)
