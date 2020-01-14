# 商品列表页分析

<img src="/goods/images/52列表页界面.png" style="zoom:50%">

### 1. 商品列表页组成结构分析

> **1.商品频道分类**

* 已经提前封装在`contents.utils.py`文件中，直接调用即可。

> **2.面包屑导航**

* 可以使用三级分类ID，查询出该类型商品的三级分类数据。

> **3.排序和分页**

* 无论如何排序和分页，商品的分类不能变。
* 排序时需要知道当前排序方式。
* 分页时需要知道当前分页的页码，且每页五条商品记录。

> **4.热销排行**

* 热销排行中的商品分类要和排序、分页的商品分类一致。
* 热销排行是查询出指定分类商品销量前二的商品。
* 热销排行使用Ajax实现局部刷新的效果。

### 2. 商品列表页接口设计和定义

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | GET |
| **请求地址** | /list/(?P&lt;category_id&gt;\d+)/(?P&lt;page_num&gt;\d+)/?sort=排序方式 |

```python
# 按照商品创建时间排序
http://www.meiduo.site:8000/list/115/1/?sort=default
# 按照商品价格由低到高排序
http://www.meiduo.site:8000/list/115/1/?sort=price
# 按照商品销量由高到低排序
http://www.meiduo.site:8000/list/115/1/?sort=hot
```

> **2.请求参数：路径参数 和 查询参数**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **category_id** | string | 是 | 商品分类ID，第三级分类 |
| **page_num** | string | 是 | 当前页码 |
| **sort** | string | 否 | 排序方式 |

> **3.响应结果：HTML**

```python
list.html
```

> **4.接口定义**

```python
class ListView(View):
    """商品列表页"""

    def get(self, request, category_id, page_num):
        """提供商品列表页"""
        return render(request, 'list.html')
```