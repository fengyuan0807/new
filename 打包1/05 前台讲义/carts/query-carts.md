# 展示购物车

<img src="/carts/images/04展示购物车2.png" style="zoom:50%">

### 1. 展示购物车接口设计和定义

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | GET |
| **请求地址** | /carts/ |

> **2.请求参数：**

```
无
```

> **3.响应结果：HTML**

```
cart.html
```

> **4.后端接口定义**

```python
class CartsView(View):
    """购物车管理"""
    
    def get(self, request):
        """展示购物车"""
        user = request.user
        if user.is_authenticated:
            # 用户已登录，查询redis购物车
            pass
        else:
            # 用户未登录，查询cookies购物车
            pass
```

### 2. 展示购物车后端逻辑实现

> **1.查询Redis购物车**

```python
class CartsView(View):
    """购物车管理"""

    def get(self, request):
        """展示购物车"""
        user = request.user
        if user.is_authenticated:
            # 用户已登录，查询redis购物车
            redis_conn = get_redis_connection('carts')
            # 获取redis中的购物车数据
            redis_cart = redis_conn.hgetall('carts_%s' % user.id)
            # 获取redis中的选中状态
            cart_selected = redis_conn.smembers('selected_%s' % user.id)

            # 将redis中的数据构造成跟cookie中的格式一致，方便统一查询
            cart_dict = {}
            for sku_id, count in redis_cart.items():
                cart_dict[int(sku_id)] = {
                    'count': int(count),
                    'selected': sku_id in cart_selected
                }
        else:
            # 用户未登录，查询cookies购物车
            pass
```

> **2.查询cookie购物车**

```python
class CartsView(View):
    """购物车管理"""

    def get(self, request):
        """展示购物车"""
        user = request.user
        if user.is_authenticated:
            # 用户已登录，查询redis购物车
            ......
        else:
            # 用户未登录，查询cookies购物车
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict = {}
```

> **3.查询购物车SKU信息**

```python
class CartsView(View):
    """购物车管理"""

    def get(self, request):
        """展示购物车"""
        user = request.user
        if user.is_authenticated:
            # 用户已登录，查询redis购物车
            ......
        else:
            # 用户未登录，查询cookies购物车
            ......

        # 构造购物车渲染数据
        sku_ids = cart_dict.keys()
        skus = models.SKU.objects.filter(id__in=sku_ids)
        cart_skus = []
        for sku in skus:
            cart_skus.append({
                'id':sku.id,
                'name':sku.name,
                'count': cart_dict.get(sku.id).get('count'),
                'selected': str(cart_dict.get(sku.id).get('selected')),  # 将True，转'True'，方便json解析
                'default_image_url':sku.default_image.url,
                'price':str(sku.price), # 从Decimal('10.2')中取出'10.2'，方便json解析
                'amount':str(sku.price * cart_dict.get(sku.id).get('count')),
            })

        context = {
            'cart_skus':cart_skus,
        }

        # 渲染购物车页面
        return render(request, 'cart.html', context)
```

> **4.渲染购物车信息**

```html
<div class="total_count">全部商品<em>[[ total_count ]]</em>件</div>
<ul class="cart_list_th clearfix">
    <li class="col01">商品名称</li>
    <li class="col03">商品价格</li>
    <li class="col04">数量</li>
    <li class="col05">小计</li>
    <li class="col06">操作</li>
</ul>
<ul class="cart_list_td clearfix" v-for="(cart_sku,index) in carts" v-cloak>
    <li class="col01"><input type="checkbox" name="" v-model="cart_sku.selected" @change="update_selected(index)"></li>
    <li class="col02"><img :src="cart_sku.default_image_url"></li>
    <li class="col03">[[ cart_sku.name ]]</li>
    <li class="col05">[[ cart_sku.price ]]元</li>
    <li class="col06">
        <div class="num_add">
            <a @click="on_minus(index)" class="minus fl">-</a>
            <input v-model="cart_sku.count" @blur="on_input(index)" type="text" class="num_show fl">
            <a @click="on_add(index)" class="add fl">+</a>
        </div>
    </li>
    <li class="col07">[[ cart_sku.amount ]]元</li>
    <li class="col08"><a @click="on_delete(index)">删除</a></li>
</ul>
<ul class="settlements" v-cloak>
    <li class="col01"><input type="checkbox" name="" @change="on_selected_all" v-model="selected_all"></li>
    <li class="col02">全选</li>
    <li class="col03">合计(不含运费)：<span>¥</span><em>[[ total_selected_amount ]]</em><br>共计<b>[[ total_selected_count ]]</b>件商品</li>
    <li class="col04"><a href="place_order.html">去结算</a></li>
</ul>
```



