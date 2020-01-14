# 渲染商品搜索结果

### 1. 准备商品搜索结果页面

<img src="/goods/images/61准备搜索结果页面.png" style="zoom:50%">

### 2. 渲染商品搜索结果

> Haystack返回的数据包括：

* `query`：搜索关键字
* `paginator`：分页paginator对象
* `page`：当前页的page对象（遍历`page`中的对象，可以得到`result`对象）
* `result.objects`: 当前遍历出来的SKU对象。

```html
<div class="main_wrap clearfix">
    <div class=" clearfix">
        <ul class="goods_type_list clearfix">
            {% for result in page %}
            <li>
                {# object取得才是sku对象 #}
                <a href="/detail/{{ result.object.id }}/"><img src="{{ result.object.default_image.url }}"></a>
                <h4><a href="/detail/{{ result.object.id }}/">{{ result.object.name }}</a></h4>
                <div class="operate">
                    <span class="price">￥{{ result.object.price }}</span>
                    <span>{{ result.object.comments }}评价</span>
                </div>
            </li>
            {% else %}
                <p>没有找到您要查询的商品。</p>
            {% endfor %}
        </ul>
        <div class="pagenation">
            <div id="pagination" class="page"></div>
        </div>
    </div>
</div>
``` 

<img src="/goods/images/62渲染搜索结果.png" style="zoom:50%">

### 3. Haystack搜索结果分页

> **1.设置每页返回数据条数**

* 通过`HAYSTACK_SEARCH_RESULTS_PER_PAGE`可以控制每页显示数量
* 每页显示五条数据：`HAYSTACK_SEARCH_RESULTS_PER_PAGE = 5`

> **2.准备搜索页分页器**

```html
<div class="main_wrap clearfix">
    <div class=" clearfix">
        ......
        <div class="pagenation">
            <div id="pagination" class="page"></div>
        </div>
    </div>
</div>
``` 

```js
<script type="text/javascript">
    $(function () {
        $('#pagination').pagination({
            currentPage: {{ page.number }},
            totalPage: {{ paginator.num_pages }},
            callback:function (current) {
                {#window.location.href = '/search/?q=iphone&amp;page=1';#}
                window.location.href = '/search/?q={{ query }}&page=' + current;
            }
        })
    });
</script>
```
    
<img src="/goods/images/63搜索结果分页.png" style="zoom:50%">



