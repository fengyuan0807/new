# 保存订单基本信息和订单商品信息

### 1. 提交订单接口设计和定义

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | POST |
| **请求地址** | /orders/commit/ |

> **2.请求参数：JSON**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **address_id** | int | 是 | 用户地址编号 |
| **pay_method** | int | 是 | 用户支付方式 |

> **3.响应结果：JSON**

| 字段 | 说明 |
| ---------------- | ---------------- |
| **code** | 状态码 |
| **errmsg** | 错误信息 |
| **order_id** | 订单编号 |

> **4.后端接口定义**

```python
class OrderCommitView(LoginRequiredJSONMixin, View):
    """订单提交"""

    def post(self, request):
        """保存订单信息和订单商品信息"""
        pass
```

> 提示：

> * 订单数据分为订单基本信息和订单商品信息，二者为一对多的关系。

> * 保存到订单的数据是从Redis购物车中的已勾选的商品信息。

### 2. 保存订单基本信息

```python
class OrderCommitView(LoginRequiredJSONMixin, View):
    """提交订单"""

    def post(self, request):
        """保存订单信息和订单商品信息"""
        # 获取当前要保存的订单数据
        json_dict = json.loads(request.body.decode())
        address_id = json_dict.get('address_id')
        pay_method = json_dict.get('pay_method')
        # 校验参数
        if not all([address_id, pay_method]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断address_id是否合法
        try:
            address = Address.objects.get(id=address_id)
        except Exception:
            return http.HttpResponseForbidden('参数address_id错误')
        # 判断pay_method是否合法
        if pay_method not in [OrderInfo.PAY_METHODS_ENUM['CASH'], OrderInfo.PAY_METHODS_ENUM['ALIPAY']]:
            return http.HttpResponseForbidden('参数pay_method错误')

        # 获取登录用户
        user = request.user
        # 生成订单编号：年月日时分秒+用户编号
        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)
        # 保存订单基本信息 OrderInfo（一）
        order = OrderInfo.objects.create(
            order_id=order_id,
            user=user,
            address=address,
            total_count=0,
            total_amount=Decimal('0'),
            freight=Decimal('10.00'),
            pay_method=pay_method,
            status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'] if pay_method == OrderInfo.PAY_METHODS_ENUM['ALIPAY'] else
            OrderInfo.ORDER_STATUS_ENUM['UNSEND']
        )
        pass
```

### 3. 保存订单商品信息

```python
class OrderCommitView(LoginRequiredJSONMixin, View):
    """提交订单"""

    def post(self, request):
        """保存订单信息和订单商品信息"""
        # 获取当前保存订单时需要的信息
        ......
        
        # 保存订单基本信息 OrderInfo（一）
        ......

        # 从redis读取购物车中被勾选的商品信息
        redis_conn = get_redis_connection('carts')
        redis_cart = redis_conn.hgetall('carts_%s' % user.id)
        selected = redis_conn.smembers('selected_%s' % user.id)
        carts = {}
        for sku_id in selected:
            carts[int(sku_id)] = int(redis_cart[sku_id])
        sku_ids = carts.keys()

        # 遍历购物车中被勾选的商品信息
        for sku_id in sku_ids:
            # 查询SKU信息
            sku = SKU.objects.get(id=sku_id)
            # 判断SKU库存
            sku_count = carts[sku.id]
            if sku_count > sku.stock:
                return http.JsonResponse({'code': RETCODE.STOCKERR, 'errmsg': '库存不足'})

            # SKU减少库存，增加销量
            sku.stock -= sku_count
            sku.sales += sku_count
            sku.save()

            # 修改SPU销量
            sku.goods.sales += sku_count
            sku.goods.save()

            # 保存订单商品信息 OrderGoods（多）
            OrderGoods.objects.create(
                order=order,
                sku=sku,
                count=sku_count,
                price=sku.price,
            )

            # 保存商品订单中总价和总数量
            order.total_count += sku_count
            order.total_amount += (sku_count * sku.price)

        # 添加邮费和保存订单信息
        order.total_amount += order.freight
        order.save()

        # 清除购物车中已结算的商品
        pl = redis_conn.pipeline()
        pl.hdel('carts_%s' % user.id, *selected)
        pl.srem('selected_%s' % user.id, *selected)
        pl.execute()

        # 响应提交订单结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '下单成功', 'order_id': order.order_id})
```

