# 结算订单

<img src="/orders/images/01结算订单页面.png" style="zoom:35%">

### 1. 结算订单逻辑分析

> **结算订单是从Redis购物车中查询出被勾选的商品信息进行结算并展示。**

### 2. 结算订单接口设计和定义

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | GET |
| **请求地址** | /orders/settlement/ |

> **2.请求参数：**

```
无
```

> **3.响应结果：HTML**

```
place_order.html
```

> **4.后端接口定义**

```python
class OrderSettlementView(LoginRequiredMixin, View):
    """结算订单"""

    def get(self, request):
        """提供订单结算页面"""
        return render(request, 'place_order.html')
```

### 3. 结算订单后端逻辑实现

```python
class OrderSettlementView(LoginRequiredMixin, View):
    """结算订单"""

    def get(self, request):
        """提供订单结算页面"""
        # 获取登录用户
        user = request.user
        # 查询地址信息
        try:
            addresses = Address.objects.filter(user=request.user, is_deleted=False)
        except Address.DoesNotExist:
            # 如果地址为空，渲染模板时会判断，并跳转到地址编辑页面
            addresses = None

        # 从Redis购物车中查询出被勾选的商品信息
        redis_conn = get_redis_connection('carts')
        redis_cart = redis_conn.hgetall('carts_%s' % user.id)
        cart_selected = redis_conn.smembers('selected_%s' % user.id)
        cart = {}
        for sku_id in cart_selected:
            cart[int(sku_id)] = int(redis_cart[sku_id])

        # 准备初始值
        total_count = 0
        total_amount = Decimal(0.00)
        # 查询商品信息
        skus = SKU.objects.filter(id__in=cart.keys())
        for sku in skus:
            sku.count = cart[sku.id]
            sku.amount = sku.count * sku.price
            # 计算总数量和总金额
            total_count += sku.count
            total_amount += sku.count * sku.price
        # 补充运费
        freight = Decimal('10.00')

        # 渲染界面
        context = {
            'addresses': addresses,
            'skus': skus,
            'total_count': total_count,
            'total_amount': total_amount,
            'freight': freight,
            'payment_amount':total_amount + freight
        }

        return render(request, 'place_order.html', context)
```

### 4.结算订单页面渲染

```html
<h3 class="common_title">确认收货地址</h3>
<div class="common_list_con clearfix" id="get_site">
    <dl>
    {% if addresses %}
        <dt>寄送到：</dt>
        {% for address in addresses %}
        <dd @click="nowsite={{ address.id }}"><input type="radio" v-model="nowsite" value="{{ address.id }}">{{ address.province }} {{ address.city }} {{ address.district }} （{{ address.receiver }} 收） {{ address.mobile }}</dd>
        {% endfor %}
    {% endif %}
    </dl>
    <a href="{{ url('users:address') }}" class="edit_site">编辑收货地址</a>
</div>
<h3 class="common_title">支付方式</h3>
<div class="common_list_con clearfix">
    <div class="pay_style_con clearfix">
        <input type="radio" name="pay_method" value="1" v-model="pay_method">
        <label class="cash">货到付款</label>
        <input type="radio" name="pay_method" value="2" v-model="pay_method">
        <label class="zhifubao"></label>
    </div>
</div>
<h3 class="common_title">商品列表</h3>
<div class="common_list_con clearfix">
    <ul class="goods_list_th clearfix">
        <li class="col01">商品名称</li>
        <li class="col02">商品单位</li>
        <li class="col03">商品价格</li>
        <li class="col04">数量</li>
        <li class="col05">小计</li>
    </ul>
    {% for sku in skus %}
    <ul class="goods_list_td clearfix">
        <li class="col01">{{loop.index}}</li>
        <li class="col02"><img src="{{ sku.default_image.url }}"></li>
        <li class="col03">{{ sku.name }}</li>
        <li class="col04">台</li>
        <li class="col05">{{ sku.price }}元</li>
        <li class="col06">{{ sku.count }}</li>
        <li class="col07">{{ sku.amount }}元</li>
    </ul>
    {% endfor %}
</div>
<h3 class="common_title">总金额结算</h3>
<div class="common_list_con clearfix">
    <div class="settle_con">
        <div class="total_goods_count">共<em>{{ total_count }}</em>件商品，总金额<b>{{ total_amount }}元</b></div>
        <div class="transit">运费：<b>{{ freight }}元</b></div>
        <div class="total_pay">实付款：<b>{{ payment_amount }}元</b></div>
    </div>
</div>
<div class="order_submit clearfix">
    <a @click="on_order_submit" id="order_btn">提交订单</a>
</div>
```