# 列表页热销排行

> 根据路径参数`category_id`查询出该类型商品销量前二的商品。

> 使用Ajax实现局部刷新的效果。

### 1. 查询列表页热销排行数据

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | GET |
| **请求地址** | /hot/(?P&lt;category_id&gt;\d+)/ |

> **2.请求参数：路径参数**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **category_id** | string | 是 | 商品分类ID，第三级分类 |

> **3.响应结果：JSON**

| 字段 | 说明 |
| ---------------- | ---------------- |
| **code** | 状态码 |
| **errmsg** | 错误信息 |
| **hot_skus[ ]** | 热销SKU列表 |
| **id** | SKU编号 |
| **default_image_url** | 商品默认图片 |
| **name** | 商品名称 |
| **price** | 商品价格 |

```json
{
    "code":"0",
    "errmsg":"OK",
    "hot_skus":[
        {
            "id":6,
            "default_image_url":"http://image.meiduo.site:8888/group1/M00/00/02/CtM3BVrRbI2ARekNAAFZsBqChgk3141998",
            "name":"Apple iPhone 8 Plus (A1864) 256GB 深空灰色 移动联通电信4G手机",
            "price":"7988.00"
        },
        {
            "id":14,
            "default_image_url":"http://image.meiduo.site:8888/group1/M00/00/02/CtM3BVrRdMSAaDUtAAVslh9vkK04466364",
            "name":"华为 HUAWEI P10 Plus 6GB+128GB 玫瑰金 移动联通电信4G手机 双卡双待",
            "price":"3788.00"
        }
    ]
}
```

> **4.接口定义和实现**

```python
class HotGoodsView(View):
    """商品热销排行"""

    def get(self, request, category_id):
        """提供商品热销排行JSON数据"""
        # 根据销量倒序
        skus = models.SKU.objects.filter(category_id=category_id, is_launched=True).order_by('-sales')[:2]

        # 序列化
        hot_skus = []
        for sku in skus:
            hot_skus.append({
                'id':sku.id,
                'default_image_url':sku.default_image.url,
                'name':sku.name,
                'price':sku.price
            })

        return http.JsonResponse({'code':RETCODE.OK, 'errmsg':'OK', 'hot_skus':hot_skus})
```

### 2. 渲染列表页热销排行数据

> **1.模板数据`category_id`传递到Vue.js**

```js
<script type="text/javascript">
    let category_id = "{{ category.id }}";
</script>
```

```js
data: {
    category_id: category_id,
},
```

> **2.Ajax请求商品热销排行JSON数据**

```js
get_hot_skus(){
    if (this.category_id) {
        let url = '/hot/'+ this.category_id +'/';
        axios.get(url, {
            responseType: 'json'
        })
            .then(response => {
                this.hot_skus = response.data.hot_skus;
                for(let i=0; i<this.hot_skus.length; i++){
                    this.hot_skus[i].url = '/detail/' + this.hot_skus[i].id + '/';
                }
            })
            .catch(error => {
                console.log(error.response);
            })
    }
},
```

> **3.渲染商品热销排行界面**

```html
<div class="new_goods" v-cloak>
    <h3>热销排行</h3>
    <ul>
        <li v-for="sku in hot_skus">
            <a :href="sku.url"><img :src="sku.default_image_url"></a>
            <h4><a :href="sku.url">[[ sku.name ]]</a></h4>
            <div class="price">￥[[ sku.price ]]</div>
        </li>
    </ul>
</div>
```


