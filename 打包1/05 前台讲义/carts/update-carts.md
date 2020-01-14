# 修改购物车

**提示：在购物车页面修改购物车使用局部刷新的效果。**

### 1. 修改购物车接口设计和定义

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | PUT |
| **请求地址** | /carts/ |

> **2.请求参数：JSON**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **sku_id** | int | 是 | 商品SKU编号 |
| **count** | int | 是 | 商品数量 |
| **selected** | bool | 否 | 是否勾选 |

> **3.响应结果：JSON**

| 字段 | 说明 |
| ---------------- | ---------------- |
| **sku_id** | 商品SKU编号 |
| **count** | 商品数量 |
| **selected** | 是否勾选 |

> **4.后端接口定义**

```python
class CartsView(View):
    """购物车管理"""
    
    def put(self, request):
        """修改购物车"""
        # 接收和校验参数
        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，修改redis购物车
            pass
        else:
            # 用户未登录，修改cookie购物车
            pass
```

### 2. 修改购物车后端逻辑实现

> **1.接收和校验参数**

```python
class CartsView(View):
    """购物车管理"""

    def put(self, request):
        """修改购物车"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')
        count = json_dict.get('count')
        selected = json_dict.get('selected', True)

        # 判断参数是否齐全
        if not all([sku_id, count]):
            return http.HttpResponseForbidden('缺少必传参数')
        # 判断sku_id是否存在
        try:
            sku = models.SKU.objects.get(id=sku_id)
        except models.SKU.DoesNotExist:
            return http.HttpResponseForbidden('商品sku_id不存在')
        # 判断count是否为数字
        try:
            count = int(count)
        except Exception:
            return http.HttpResponseForbidden('参数count有误')
        # 判断selected是否为bool值
        if selected:
            if not isinstance(selected, bool):
                return http.HttpResponseForbidden('参数selected有误')

        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，修改redis购物车
            pass
        else:
            # 用户未登录，修改cookie购物车
            pass
```

> **2.修改Redis购物车**

```python
class CartsView(View):
    """购物车管理"""

    def put(self, request):
        """修改购物车"""
        # 接收和校验参数
        ......

        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，修改redis购物车
            redis_conn = get_redis_connection('carts')
            pl = redis_conn.pipeline()
            # 因为接口设计为幂等的，直接覆盖
            pl.hset('carts_%s' % user.id, sku_id, count)
            # 是否选中
            if selected:
                pl.sadd('selected_%s' % user.id, sku_id)
            else:
                pl.srem('selected_%s' % user.id, sku_id)
            pl.execute()

            # 创建响应对象
            cart_sku = {
                'id':sku_id,
                'count':count,
                'selected':selected,
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': sku.price,
                'amount': sku.price * count,
            }
            return http.JsonResponse({'code':RETCODE.OK, 'errmsg':'修改购物车成功', 'cart_sku':cart_sku})
        else:
            # 用户未登录，修改cookie购物车
            pass
```

> **3.修改cookie购物车**

```python
class CartsView(View):
    """购物车管理"""

    def put(self, request):
        """修改购物车"""
        # 接收和校验参数
        ......

        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，修改redis购物车
            ......
        else:
            # 用户未登录，修改cookie购物车
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict = {}
            # 因为接口设计为幂等的，直接覆盖
            cart_dict[sku_id] = {
                'count': count,
                'selected': selected
            }
            # 将字典转成bytes,再将bytes转成base64的bytes,最后将bytes转字符串
            cookie_cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()

            # 创建响应对象
            cart_sku = {
                'id': sku_id,
                'count': count,
                'selected': selected,
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': sku.price,
                'amount': sku.price * count,
            }
            response = http.JsonResponse({'code':RETCODE.OK, 'errmsg':'修改购物车成功', 'cart_sku':cart_sku})
            # 响应结果并将购物车数据写入到cookie
            response.set_cookie('carts', cookie_cart_str, max_age=constants.CARTS_COOKIE_EXPIRES)
            return response
```