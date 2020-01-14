# 展示商品页面简单购物车

<img src="/carts/images/05商品页右上角购物车.png" style="zoom:50%">

**需求：用户鼠标悬停在商品页面右上角购物车标签上，以下拉框形式展示当前购物车数据。**

### 1. 简单购物车数据接口设计和定义

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | GET |
| **请求地址** | /carts/simple/ |

> **2.请求参数：**

```
无
```

> **3.响应结果：JSON**

| 字段 | 说明 |
| ---------------- | ---------------- |
| **code** | 状态码 |
| **errmsg** | 错误信息 |
| **cart_skus[ ]** | 简单购物车SKU列表 |
| **id** | 购物车SKU编号 |
| **name** | 购物车SKU名称 |
| **count** | 购物车SKU数量 |
| **default_image_url** | 购物车SKU图片 |

```json
{
    "code":"0",
    "errmsg":"OK",
    "cart_skus":[
        {
            "id":1,
            "name":"Apple MacBook Pro 13.3英寸笔记本 银色",
            "count":1,
            "default_image_url":"http://image.meiduo.site:8888/group1/M00/00/02/CtM3BVrPB4GAWkTlAAGuN6wB9fU4220429"
        },
        ......
    ]
}
```

> **4.后端接口定义**

```python
class CartsSimpleView(View):
    """商品页面右上角购物车"""

    def get(self, request):
        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，查询Redis购物车
            pass
        else:
            # 用户未登录，查询cookie购物车
            pass

        # 构造简单购物车JSON数据
        pass
```

### 2. 简单购物车数据后端逻辑实现

> **1.查询Redis购物车**

```python
class CartsSimpleView(View):
    """商品页面右上角购物车"""

    def get(self, request):
        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，查询Redis购物车
            redis_conn = get_redis_connection('carts')
            redis_cart = redis_conn.hgetall('carts_%s' % user.id)
            cart_selected = redis_conn.smembers('selected_%s' % user.id)
            # 将redis中的两个数据统一格式，跟cookie中的格式一致，方便统一查询
            cart_dict = {}
            for sku_id, count in redis_cart.items():
                cart_dict[int(sku_id)] = {
                    'count': int(count),
                    'selected': sku_id in cart_selected
                }
        else:
            # 用户未登录，查询cookie购物车
            pass

        # 构造简单购物车JSON数据
        pass
```

> **2.查询Redis购物车**

```python
class CartsSimpleView(View):
    """商品页面右上角购物车"""

    def get(self, request):
        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，查询Redis购物车
            ......
        else:
            # 用户未登录，查询cookie购物车
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict = {}
```

> **3.构造简单购物车JSON数据**

```python
class CartsSimpleView(View):
    """商品页面右上角购物车"""

    def get(self, request):
        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，查询Redis购物车
            ......
        else:
            # 用户未登录，查询cookie购物车
            ......

        # 构造简单购物车JSON数据
        cart_skus = []
        sku_ids = cart_dict.keys()
        skus = models.SKU.objects.filter(id__in=sku_ids)
        for sku in skus:
            cart_skus.append({
                'id':sku.id,
                'name':sku.name,
                'count':cart_dict.get(sku.id).get('count'),
                'default_image_url': sku.default_image.url
            })

        # 响应json列表数据
        return http.JsonResponse({'code':RETCODE.OK, 'errmsg':'OK', 'cart_skus':cart_skus})
```

### 3. 展示商品页面简单购物车

> **1.商品页面发送Ajax请求**
* `index.js`、`list.js`、`detail.js`

```js
get_carts(){
    let url = '/carts/simple/';
    axios.get(url, {
        responseType: 'json',
    })
        .then(response => {
            this.carts = response.data.cart_skus;
            this.cart_total_count = 0;
            for(let i=0;i<this.carts.length;i++){
                if (this.carts[i].name.length>25){
                    this.carts[i].name = this.carts[i].name.substring(0, 25) + '...';
                }
                this.cart_total_count += this.carts[i].count;
            }
        })
        .catch(error => {
            console.log(error.response);
        })
},
```

> **2.商品页面渲染简单购物车数据**
* `index.html`、`list.html`、`detail.html`

```html
<div @mouseenter="get_carts" class="guest_cart fr" v-cloak>
    <a href="{{ url('carts:info') }}" class="cart_name fl">我的购物车</a>
    <div class="goods_count fl" id="show_count">[[ cart_total_count ]]</div>
    <ul class="cart_goods_show">
        <li v-for="sku in carts">
            <img :src="sku.default_image_url" alt="商品图片">
            <h4>[[ sku.name ]]</h4>
            <div>[[ sku.count ]]</div>
        </li>
    </ul>
</div>
```





