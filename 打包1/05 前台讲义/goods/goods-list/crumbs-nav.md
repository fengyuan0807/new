# 列表页面包屑导航
 
> 重要提示：路径参数**category_id**是商品**第三级分类**
 
### 1. 查询列表页面包屑导航数据
 
> 提示： 对包屑导航数据的查询进行封装，方便后续直接使用。

> `goods.utils.py`
 
```python
def get_breadcrumb(category):
    """
    获取面包屑导航
    :param category: 商品类别
    :return: 面包屑导航字典
    """
    breadcrumb = dict(
        cat1='',
        cat2='',
        cat3=''
    )
    if category.parent is None:
        # 当前类别为一级类别
        breadcrumb['cat1'] = category
    elif category.subs.count() == 0:
        # 当前类别为三级
        breadcrumb['cat3'] = category
        cat2 = category.parent
        breadcrumb['cat2'] = cat2
        breadcrumb['cat1'] = cat2.parent
    else:
        # 当前类别为二级
        breadcrumb['cat2'] = category
        breadcrumb['cat1'] = category.parent

    return breadcrumb
```

```python
class ListView(View):
    """商品列表页"""

    def get(self, request, category_id, page_num):
        """提供商品列表页"""
        # 判断category_id是否正确
        try:
            category = models.GoodsCategory.objects.get(id=category_id)
        except models.GoodsCategory.DoesNotExist:
            return http.HttpResponseNotFound('GoodsCategory does not exist')

        # 查询商品频道分类
        categories = get_categories()
        # 查询面包屑导航
        breadcrumb = get_breadcrumb(category)

        # 渲染页面
        context = {
            'categories':categories,
            'breadcrumb':breadcrumb
        }
        return render(request, 'list.html', context)
```
 
### 2. 渲染列表页面包屑导航数据
 
```html
<div class="breadcrumb">
    <a href="{{ breadcrumb.cat1.url }}">{{ breadcrumb.cat1.name }}</a>
    <span>></span>
    <a href="javascript:;">{{ breadcrumb.cat2.name }}</a>
    <span>></span>
    <a href="javascript:;">{{ breadcrumb.cat3.name }}</a>
</div>
```
