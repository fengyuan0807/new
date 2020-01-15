from django.shortcuts import render
from django.views import View
import json, logging
from django import http
from django_redis import get_redis_connection

from .utils import str_to_dict, dict_to_str
from meiduo_mall.utils.response_code import RETCODE
from goods.models import SKU

# Create your views here.
logger = logging.getLogger('django')


class CartsSimpleView(View):
    """页面简单购物车"""

    def get(self, request):

        user = request.user
        if user.is_authenticated:
            redis_conn = get_redis_connection('carts')
            redis_cart = redis_conn.hgetall('carts_%s' % user.id)
            # carts_user_id: {sku_id1: count, sku_id3: count, sku_id5: count, ...}
            cart_selected = redis_conn.smembers('selected_%s' % user.id)
            # selected_user_id: [sku_id1, sku_id3, ...]
            """
            {
                11: {
                    "count": "1",
                    "selected": "True"
                },
                22: {
                    "count": "3",
                    "selected": "True"
                },
            }
            """
            # 注意是bytes格式需要转,构造一个和cookie中的格式一致，方便查询
            cart_dict = {}
            for sku_id, count in redis_cart.items():
                cart_dict[int(sku_id)] = {
                    'count': int(count),
                    'selected': sku_id in cart_selected
                }
        else:
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                cart_dict = str_to_dict(cart_str)
            else:
                cart_dict = {}
        # {
        #     "code": "0",
        #     "errmsg": "OK",
        #     "cart_skus": [
        #         {
        #             "id": 1,
        #             "name": "Apple MacBook Pro 13.3英寸笔记本 银色",
        #             "count": 1,
        #             "default_image_url": "http://image.meiduo.site:8888/group1/M00/00/02/CtM3BVrPB4GAWkTlAAGuN6wB9fU4220429"
        #         },
        #         ......
        #     ]
        # }
        sku_ids = cart_dict.keys()
        # for sku_id in sku_ids:
        #     sku = SKU.objects.get(id=sku_id)
        skus = SKU.objects.filter(id__in=sku_ids)
        cart_skus = []
        for sku in skus:
            cart_skus.append({
                "id": sku.id,
                "name": sku.name,
                "count": cart_dict[sku.id]['count'],
                "default_image_url": sku.default_image.url,
            })
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'cart_skus': cart_skus})


class CartsSelectAllView(View):
    """全选,取消全选"""

    def put(self, request):
        json_dict = json.loads(request.body.decode())
        selected = json_dict.get('selected', True)
        if selected:
            if not isinstance(selected, bool):
                return http.HttpResponseForbidden('参数selected有误')
        user = request.user
        if user.is_authenticated:
            redis_conn = get_redis_connection('carts')
            # 取出来的是这样的{b'2':b'3',b'3':'5'}
            redis_cart = redis_conn.hgetall('carts_%s' % user.id)
            sku_id_list = redis_cart.keys()
            if selected:
                # 全选
                redis_conn.sadd('selected_%s' % user.id, *sku_id_list)
            else:
                # 取消全选
                redis_conn.srem('selected_%s' % user.id, *sku_id_list)
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})
        else:
            carts_str = request.COOKIES.get('carts')
            response = http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})
            if carts_str:
                carts_dict = str_to_dict(carts_str)
                # """
                #  {
                #      11(sku_id): {
                #          "count": "1",
                #          "selected": "True"
                #      },
                #      22: {
                #          "count": "3",
                #          "selected": "True"
                #      },
                #  }
                #  """
                for sku_id in carts_dict.keys():
                    carts_dict[sku_id]['selected'] = selected
                cookie_cart_str = dict_to_str(carts_dict)
                response.set_cookie('carts', cookie_cart_str)
            return response


class CartsView(View):
    def post(self, request):
        """添加购物车"""
        # 接受 校验参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        count = json_dict.get('count')
        selected = json_dict.get('selected', True)
        if not all([sku_id, count]):
            return http.HttpResponseForbidden('缺少必传参数')
        try:
            SKU.objects.get(id=sku_id)
        except SKU.DoseNotExist:
            return http.HttpResponseForbidden('sku_id不正确')
            # 判断counts是否是数字
        try:
            count = int(count)
        except Exception as e:
            logger.error(e)
            return http.HttpResponseForbidden('count不正确')
        if selected:
            if not isinstance(selected, bool):
                return http.HttpResponseForbidden('selected不正确')
        # 判断用户书否登陆
        user = request.user
        if user.is_authenticated:
            # 用户登陆的话操作 redis 购物车
            # carts_user_id: {sku_id1: count, sku_id3: count, sku_id5: count, ...}
            # selected_user_id: [sku_id1, sku_id3, ...]
            redis_conn = get_redis_connection('carts')
            pl = redis_conn.pipeline()
            # 新增购物车数据
            # 当要添加到购物车的商品已存在时，对商品数量进行累加计算。
            # 当要添加到购物车的商品不存在时，向hash中新增field和value即可。
            # 这里hincrby：主动count+1,hash 结构 键 属性 值
            pl.hincrby('carts_%s' % user.id, sku_id, count)
            # 新增选中的状态
            if selected:
                pl.sadd('selected_%s' % user.id, sku_id)
            pl.execute()
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})

        else:
            # 用户未登录的话操作 cookie 购物车
            """
            {
                11: {
                    "count": "1",
                    "selected": "True"
                },
                22: {
                    "count": "3",
                    "selected": "True"
                },
            }
            """
            cart_str = request.COOKIES.get('carts')
            # 如果操作过cookie购物车
            if cart_str:
                # 转成字典数据
                cart_dict = str_to_dict(cart_str)
            # 没有操作的话
            else:
                cart_dict = {}
            # 判断要加入的购物车商品是否已经存在在购物车中
            # 当要添加到购物车的商品已存在时，对商品数量进行累加计算。
            if sku_id in cart_dict.keys():
                origin_count = cart_dict.get(sku_id).get('count')
                count += origin_count
            # 当要添加到购物车的商品不存在时，向JSON中新增field和value即可。
            cart_dict[sku_id] = {
                'count': count,
                'selected': selected
            }
            # 把dict数据序列化
            cookie_cart_str = dict_to_str(cart_dict)
            # 设置到cookie中
            response = http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})
            response.set_cookie('carts', cookie_cart_str)
            return response

    def get(self, request):
        """展示购物车"""
        user = request.user
        if user.is_authenticated:
            # 操作redis数据库购物车
            redis_conn = get_redis_connection('carts')
            # 获取redis中的购物车数据(b'1':b'3')
            redis_cart = redis_conn.hgetall('carts_%s' % user.id)
            # 获取redis中的selected(b'2',b'3')
            cart_selected = redis_conn.smembers('selected_%s' % user.id)

            # 将redis中的数据构造成跟cookie中的格式一致，方便统一查询
            cart_dict = {}
            """
            {
                11: {
                    "count": "1",
                    "selected": "True"
                },
                22: {
                    "count": "3",
                    "selected": "True"
                },
            }
            """
            for sku_id, count in redis_cart.items():
                cart_dict[int(sku_id)] = {
                    'count': int(count),
                    'selected': sku_id in cart_selected
                }

        else:
            # 操作 cookie
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                cart_dict = str_to_dict(cart_str)
            else:
                cart_dict = {}
        sku_ids = cart_dict.keys()
        skus = SKU.objects.filter(id__in=sku_ids)
        cart_skus = []
        for sku in skus:
            cart_skus.append({
                'id': sku.id,
                'name': sku.name,
                'count': cart_dict.get(sku.id).get('count'),
                'selected': str(cart_dict.get(sku.id).get('selected')),  # 将True，转'True'，方便json解析
                'default_image_url': sku.default_image.url,
                'price': str(sku.price),  # 从Decimal('10.2')中取出'10.2'，方便json解析
                'amount': str(sku.price * cart_dict.get(sku.id).get('count'))
            })
        context = {
            'cart_skus': cart_skus
        }
        return render(request, 'cart.html', context)

    def put(self, request):
        """修改购物车"""
        # 接受 校验参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        count = json_dict.get('count')
        selected = json_dict.get('selected', True)
        if not all([sku_id, count]):
            return http.HttpResponseForbidden('缺少必传参数')
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoseNotExist:
            return http.HttpResponseForbidden('sku_id不正确')
            # 判断counts是否是数字
        try:
            count = int(count)
        except Exception as e:
            logger.error(e)
            return http.HttpResponseForbidden('count不正确')
        if selected:
            if not isinstance(selected, bool):
                return http.HttpResponseForbidden('selected不正确')
        user = request.user
        if user.is_authenticated:
            redis_conn = get_redis_connection('carts')
            pl = redis_conn.pipeline()
            pl.hset('carts_%s' % user.id, sku_id, count)
            if selected:
                pl.sadd('selected_%s' % user.id, sku_id)
            else:
                pl.srem('selected_%s' % user.id, sku_id)
            pl.execute()
            cart_sku = {
                'id': sku_id,
                'count': count,
                'selected': selected,
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': sku.price,
                'amount': sku.price * count
            }
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'cart_sku': cart_sku})
        else:
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                cart_dict = str_to_dict(cart_str)
            else:
                cart_dict = {}
            cart_dict[sku_id] = {
                'count': count,
                'selected': selected
            }
            cookie_cart_str = dict_to_str(cart_dict)
            cart_sku = {
                'id': sku_id,
                'count': count,
                'selected': selected,
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': sku.price,
                'amount': sku.price * count
            }
            response = http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok', 'cart_sku': cart_sku})
            response.set_cookie('carts', cookie_cart_str)
            return response

    def delete(self, request):
        """删除购物车数据"""
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return http.HttpResponseForbidden('sku_id不正确')
        user = request.user
        if user.is_authenticated:
            redis_conn = get_redis_connection('carts')
            pl = redis_conn.pipeline()
            pl.hdel('carts_%s' % user.id, sku_id)
            pl.srem('selected_%s' % user.id, sku_id)
            pl.execute()
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '删除购物车成功'})
        else:
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                cart_dict = str_to_dict(cart_str)
            else:
                cart_dict = {}
            response = http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})
            if sku_id in cart_dict.keys():
                """
              {
                  11(sku_id): {
                      "count": "1",
                      "selected": "True"
                  },
                  22: {
                      "count": "3",
                      "selected": "True"
                  },
              }
              """
                # del cart_dict.get(sku_id)
                del cart_dict[sku_id]  # 只能这么删除
                cookie_cart_str = dict_to_str(cart_dict)
                response.set_cookie('carts', cookie_cart_str)
            return response
