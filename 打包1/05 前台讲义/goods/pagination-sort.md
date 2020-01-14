# 列表页分页和排序

```python
# 按照商品创建时间排序
http://www.meiduo.site:8000/list/115/1/?sort=default
# 按照商品价格由低到高排序
http://www.meiduo.site:8000/list/115/1/?sort=price
# 按照商品销量由高到低排序
http://www.meiduo.site:8000/list/115/1/?sort=hot
```

### 1. 查询列表页分页和排序数据

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
        # 接收sort参数：如果用户不传，就是默认的排序规则
        sort = request.GET.get('sort', 'default')

        # 查询商品频道分类
        categories = get_categories()
        # 查询面包屑导航
        breadcrumb = get_breadcrumb(category)

        # 按照排序规则查询该分类商品SKU信息
        if sort == 'price':
            # 按照价格由低到高
            sort_field = 'price'
        elif sort == 'hot':
            # 按照销量由高到低
            sort_field = '-sales'
        else:
            # 'price'和'sales'以外的所有排序方式都归为'default'
            sort = 'default'
            sort_field = 'create_time'
        skus = models.SKU.objects.filter(category=category, is_launched=True).order_by(sort_field)

        # 创建分页器：每页N条记录
        paginator = Paginator(skus, constants.GOODS_LIST_LIMIT)
        # 获取每页商品数据
        try:
            page_skus = paginator.page(page_num)
        except EmptyPage:
            # 如果page_num不正确，默认给用户404
            return http.HttpResponseNotFound('empty page')
        # 获取列表页总页数
        total_page = paginator.num_pages

        # 渲染页面
        context = {
            'categories': categories,   # 频道分类
            'breadcrumb': breadcrumb,   # 面包屑导航
            'sort': sort,               # 排序字段
            'category': category,       # 第三级分类
            'page_skus': page_skus,     # 分页后数据
            'total_page': total_page,   # 总页数
            'page_num': page_num,       # 当前页码
        }
        return render(request, 'list.html', context)
```

### 2. 渲染列表页分页和排序数据

> **1.渲染分页和排序数据**

```html
<div class="r_wrap fr clearfix">
    <div class="sort_bar">
        <a href="{{ url('goods:list', args=(category.id, page_num)) }}?sort=default" {% if sort == 'default' %}class="active"{% endif %}>默认</a>
        <a href="{{ url('goods:list', args=(category.id, page_num)) }}?sort=price" {% if sort == 'price' %}class="active"{% endif %}>价格</a>
        <a href="{{ url('goods:list', args=(category.id, page_num)) }}?sort=hot" {% if sort == 'hot' %}class="active"{% endif %}>人气</a>
    </div>
    <ul class="goods_type_list clearfix">
        {% for sku in page_skus %}
        <li>
        <a href="detail.html"><img src="{{ sku.default_image.url }}"></a>
        <h4><a href="detail.html">{{ sku.name }}</a></h4>
        <div class="operate">
            <span class="price">￥{{ sku.price }}</span>
            <span class="unit">台</span>
            <a href="#" class="add_goods" title="加入购物车"></a>
        </div>
        </li>
        {% endfor %}
    </ul>
</div>
```

> **2.列表页分页器**

<img src="/goods/images/53分页器.png" style="zoom:50%">

> 准备分页器标签

```html
<div class="r_wrap fr clearfix">
    ......
    <div class="pagenation">
        <div id="pagination" class="page"></div>
    </div>
</div>
```

```html
# 导入样式时放在最前面导入
<link rel="stylesheet" type="text/css" href="{{ static('css/jquery.pagination.css') }}">
```

> 准备分页器交互

```js
<script type="text/javascript" src="{{ static('js/jquery.pagination.min.js') }}"></script>
```

```js
<script type="text/javascript">
    $(function () {
        $('#pagination').pagination({
            currentPage: {{ page_num }},
            totalPage: {{ total_page }},
            callback:function (current) {
                {#location.href = '/list/115/1/?sort=default';#}
                location.href = '/list/{{ category.id }}/' + current + '/?sort={{ sort }}';
            }
        })
    });
</script>
```


