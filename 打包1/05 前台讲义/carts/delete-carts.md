# 删除购物车

**提示：在购物车页面删除购物车使用局部刷新的效果。**

### 1. 删除购物车接口设计和定义

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | DELETE |
| **请求地址** | /carts/ |

> **2.请求参数：JSON**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **sku_id** | int | 是 | 商品SKU编号 |

> **3.响应结果：JSON**

| 字段 | 说明 |
| ---------------- | ---------------- |
| **code** | 状态码 |
| **errmsg** | 错误信息 |

> **4.后端接口定义**

```python
class CartsView(View):
    """购物车管理"""
    
    def delete(self, request):
        """删除购物车"""
        # 接收和校验参数
        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，删除redis购物车
            pass
        else:
            # 用户未登录，删除cookie购物车
            pass
```

### 2. 删除购物车后端逻辑实现

> **1.接收和校验参数**

```python
class CartsView(View):
    """购物车管理"""

    def delete(self, request):
        """删除购物车"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')

        # 判断sku_id是否存在
        try:
            models.SKU.objects.get(id=sku_id)
        except models.SKU.DoesNotExist:
            return http.HttpResponseForbidden('商品不存在')

        # 判断用户是否登录
        user = request.user
        if user is not None and user.is_authenticated:
            # 用户未登录，删除redis购物车
            pass
        else:
            # 用户未登录，删除cookie购物车
            pass
```

> **2.删除Redis购物车**

```python
class CartsView(View):
    """购物车管理"""

    def delete(self, request):
        """删除购物车"""
        # 接收和校验参数
        ......

        # 判断用户是否登录
        user = request.user
        if user is not None and user.is_authenticated:
            # 用户未登录，删除redis购物车
            redis_conn = get_redis_connection('carts')
            pl = redis_conn.pipeline()
            # 删除键，就等价于删除了整条记录
            pl.hdel('carts_%s' % user.id, sku_id)
            pl.srem('selected_%s' % user.id, sku_id)
            pl.execute()

            # 删除结束后，没有响应的数据，只需要响应状态码即可
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '删除购物车成功'})
        else:
            # 用户未登录，删除cookie购物车
            pass
```

> **3.删除cookie购物车**

```python
class CartsView(View):
    """购物车管理"""

    def delete(self, request):
        """删除购物车"""
        # 接收和校验参数
        ......

        # 判断用户是否登录
        user = request.user
        if user is not None and user.is_authenticated:
            # 用户未登录，删除redis购物车
            ......
        else:
            # 用户未登录，删除cookie购物车
            cart_str = request.COOKIES.get('carts')
            if cart_str:
                # 将cart_str转成bytes,再将bytes转成base64的bytes,最后将bytes转字典
                cart_dict = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart_dict = {}

            # 创建响应对象
            response = http.JsonResponse({'code': RETCODE.OK, 'errmsg': '删除购物车成功'})
            if sku_id in cart_dict:
                del cart_dict[sku_id]
                # 将字典转成bytes,再将bytes转成base64的bytes,最后将bytes转字符串
                cookie_cart_str = base64.b64encode(pickle.dumps(cart_dict)).decode()
                # 响应结果并将购物车数据写入到cookie
                response.set_cookie('carts', cookie_cart_str, max_age=constants.CARTS_COOKIE_EXPIRES)
            return response
```