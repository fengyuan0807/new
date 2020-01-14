# 商品详情页分析和准备

<img src="/goods/images/64商品详情页.png" style="zoom:50%">

### 1. 商品详情页组成结构分析

> **1.商品频道分类**

* 已经提前封装在`contents.utils.py`文件中，直接调用方法即可。

> **2.面包屑导航**

* 已经提前封装在`goods.utils.py`文件中，直接调用方法即可。

> **3.热销排行**

* 该接口已经在商品列表页中实现完毕，前端直接调用接口即可。

> **4.商品SKU信息(详情信息)**

* 通过`sku_id`可以找到SKU信息，然后渲染模板即可。
* 使用Ajax实现局部刷新效果。

> **5.SKU规格信息**

* 通过`SKU`可以找到SPU规格和SKU规格信息。

> **6.商品详情介绍、规格与包装、售后服务**

* 通过`SKU`可以找到`SPU`信息，`SPU`中可以查询出商品详情介绍、规格与包装、售后服务。

> **7.商品评价**

* 商品评价需要在生成了订单，对订单商品进行评价后再实现，商品评价信息是动态数据。
* 使用Ajax实现局部刷新效果。

### 2. 商品详情页接口设计和定义

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | GET |
| **请求地址** | /detail/(?P&lt;sku_id&gt;\d+)/ |

> **2.请求参数：路径参数**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **sku_id** | string | 是 | 商品SKU编号 |

> **3.响应结果：HTML**

```python
detail.html
```

> **4.接口定义**

```python
class DetailView(View):
    """商品详情页"""

    def get(self, request, sku_id):
        """提供商品详情页"""
        return render(request, 'detail.html')
```

### 3. 商品详情页初步渲染

> 渲染商品频道分类、面包屑导航、商品热销排行
* 将原先在商品列表页实现的代码拷贝到商品详情页即可。
* 添加`detail.js`

```python
class DetailView(View):
    """商品详情页"""

    def get(self, request, sku_id):
        """提供商品详情页"""
        # 获取当前sku的信息
        try:
            sku = models.SKU.objects.get(id=sku_id)
        except models.SKU.DoesNotExist:
            return render(request, '404.html')

        # 查询商品频道分类
        categories = get_categories()
        # 查询面包屑导航
        breadcrumb = get_breadcrumb(sku.category)

        # 渲染页面
        context = {
            'categories':categories,
            'breadcrumb':breadcrumb,
            'sku':sku,
        }
        return render(request, 'detail.html', context)
```

> 提示：为了让前端在获取商品热销排行数据时，能够拿到商品分类ID，我们将商品分类ID从模板传入到Vue.js

```html
<script type="text/javascript">
    let category_id = "{{ sku.category.id }}";
</script>
```

```js
data: {
    category_id: category_id,
},
```