# 保存和查询浏览记录

### 1. 保存用户浏览记录

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | POST |
| **请求地址** | /browse_histories/ |

> **2.请求参数：JSON**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **sku_id** | string | 是 | 商品SKU编号 |

> **3.响应结果：JSON**

| 字段 | 说明 |
| ---------------- | ---------------- |
| **code** | 状态码 |
| **errmsg** | 错误信息 |

> **4.后端接口定义和实现**

```python
class UserBrowseHistory(LoginRequiredJSONMixin, View):
    """用户浏览记录"""

    def post(self, request):
        """保存用户浏览记录"""
        # 接收参数
        json_dict = json.loads(request.body.decode())
        sku_id = json_dict.get('sku_id')

        # 校验参数
        try:
            models.SKU.objects.get(id=sku_id)
        except models.SKU.DoesNotExist:
            return http.HttpResponseForbidden('sku不存在')

        # 保存用户浏览数据
        redis_conn = get_redis_connection('history')
        pl = redis_conn.pipeline()
        user_id = request.user.id

        # 先去重
        pl.lrem('history_%s' % user_id, 0, sku_id)
        # 再存储
        pl.lpush('history_%s' % user_id, sku_id)
        # 最后截取
        pl.ltrim('history_%s' % user_id, 0, 4)
        # 执行管道
        pl.execute()

        # 响应结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})
```

### 2. 查询用户浏览记录

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | GET |
| **请求地址** | /browse_histories/ |

> **2.请求参数：**

```
无
```

> **3.响应结果：JSON**

| 字段 | 说明 |
| ---------------- | ---------------- |
| **code** | 状态码 |
| **errmsg** | 错误信息 |
| **skus[ ]** | 商品SKU列表数据 |
| **id** | 商品SKU编号 |
| **name** | 商品SKU名称 |
| **default_image_url** | 商品SKU默认图片 |
| **price** | 商品SKU单价 |

```json
{
    "code":"0",
    "errmsg":"OK",
    "skus":[
        {
            "id":6,
            "name":"Apple iPhone 8 Plus (A1864) 256GB 深空灰色 移动联通电信4G手机",
            "default_image_url":"http://image.meiduo.site:8888/group1/M00/00/02/CtM3BVrRbI2ARekNAAFZsBqChgk3141998",
            "price":"7988.00"
        },
        ......
    ]
}
```

> **4.后端接口定义和实现**

```python
class UserBrowseHistory(LoginRequiredJSONMixin, View):
    """用户浏览记录"""

    def get(self, request):
        """获取用户浏览记录"""
        # 获取Redis存储的sku_id列表信息
        redis_conn = get_redis_connection('history')
        sku_ids = redis_conn.lrange('history_%s' % request.user.id, 0, -1)

        # 根据sku_ids列表数据，查询出商品sku信息
        skus = []
        for sku_id in sku_ids:
            sku = models.SKU.objects.get(id=sku_id)
            skus.append({
                'id': sku.id,
                'name': sku.name,
                'default_image_url': sku.default_image.url,
                'price': sku.price
            })

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'skus': skus})
```

> Vue渲染用户浏览记录

```html
<div class="has_view_list" v-cloak>
    <ul class="goods_type_list clearfix">
        <li v-for="sku in histories">
            <a :href="sku.url"><img :src="sku.default_image_url"></a>
            <h4><a :href="sku.url">[[ sku.name ]]</a></h4>
            <div class="operate">
                <span class="price">￥[[ sku.price ]]</span>
                <span class="unit">台</span>
                <a href="javascript:;" class="add_goods" title="加入购物车"></a>
            </div>
        </li>
    </ul>
</div>
```

<img src="/goods/images/70浏览记录展示效果.png" style="zoom:50%">
