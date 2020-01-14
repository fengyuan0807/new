# 全选购物车

**提示：在购物车页面修改购物车使用局部刷新的效果。**

### 1. 全选购物车接口设计和定义

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | PUT |
| **请求地址** | /carts/selection/ |

> **2.请求参数：JSON**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **selected** | bool | 是 | 是否全选 |

> **3.响应结果：JSON**

| 字段 | 说明 |
| ---------------- | ---------------- |
| **code** | 状态码 |
| **errmsg** | 错误信息 |

> **4.后端接口定义**

```python
class CartsSelectAllView(View):
    """全选购物车"""
    
    def put(self, request):
        # 接收和校验参数
        # 判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 用户已登录，操作redis购物车
            pass
        else:
            # 用户未登录，操作cookie购物车
            pass
```

### 2. 全选购物车后端逻辑实现

> **1.接收和校验参数**

```python
class CartsSelectAllView(View):
    """全选购物车"""

    def put(self, request):
        # 接收参数
        json_dict = json.loads(request.body.decode())
        selected = json_dict.get('selected', True)

        # 校验参数
        if selected:
            if not isinstance(selected, bool):
                return http.HttpResponseForbidden('参数selected有误')

        # 判断用户是否登录
        user = request.user
        if user is not None and user.is_authenticated:
            # 用户已登录，操作redis购物车
            pass
        else:
            # 用户已登录，操作cookie购物车
            pass
```

> **2.全选Redis购物车**

```python
class CartsSelectAllView(View):
    """全选购物车"""

    def put(self, request):
        # 接收和校验参数
        ......

        # 判断用户是否登录
        user = request.user
        if user is not None and user.is_authenticated:
            # 用户已登录，操作redis购物车
            redis_conn = get_redis_connection('carts')
            cart = redis_conn.hgetall('carts_%s' % user.id)
            sku_id_list = cart.keys()
            if selected:
                # 全选
                redis_conn.sadd('selected_%s' % user.id, *sku_id_list)
            else:
                # 取消全选
                redis_conn.srem('selected_%s' % user.id, *sku_id_list)
            return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '全选购物车成功'})
        else:
            # 用户已登录，操作cookie购物车
            pass
```

> **3.全选cookie购物车**

```python
class CartsSelectAllView(View):
    """全选购物车"""

    def put(self, request):
        # 接收和校验参数
        ......

        # 判断用户是否登录
        user = request.user
        if user is not None and user.is_authenticated:
            # 用户已登录，操作redis购物车
            ......
        else:
            # 用户已登录，操作cookie购物车
            cart = request.COOKIES.get('carts')
            response = http.JsonResponse({'code': RETCODE.OK, 'errmsg': '全选购物车成功'})
            if cart is not None:
                cart = pickle.loads(base64.b64decode(cart.encode()))
                for sku_id in cart:
                    cart[sku_id]['selected'] = selected
                cookie_cart = base64.b64encode(pickle.dumps(cart)).decode()
                response.set_cookie('carts', cookie_cart, max_age=constants.CARTS_COOKIE_EXPIRES)

            return response
```