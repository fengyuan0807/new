# 展示详情页数据

### 1. 查询和渲染SKU详情信息

```python
# 渲染页面
context = {
    'categories':categories,
    'breadcrumb':breadcrumb,
    'sku':sku,
}
return render(request, 'detail.html', context)
```

```html
<div class="goods_detail_con clearfix">
    <div class="goods_detail_pic fl"><img src="{{ sku.default_image.url }}"></div>
    <div class="goods_detail_list fr">
        <h3>{{ sku.name }}</h3>
        <p>{{ sku.caption }}</p>
        <div class="price_bar">
            <span class="show_pirce">¥<em>{{ sku.price }}</em></span>
            <a href="javascript:;" class="goods_judge">18人评价</a>
        </div>
        <div class="goods_num clearfix">
            <div class="num_name fl">数 量：</div>
            <div class="num_add fl">
                <input v-model="sku_count" @blur="check_sku_count" type="text" class="num_show fl">
                <a @click="on_addition" class="add fr">+</a>
                <a @click="on_minus" class="minus fr">-</a>
            </div> 
        </div>
        {#...商品规格...#}
        <div class="total" v-cloak>总价：<em>[[ sku_amount ]]元</em></div>
        <div class="operate_btn">
            <a href="javascript:;" class="add_cart" id="add_cart">加入购物车</a>				
        </div>
    </div>
</div>
```

> 提示：为了实现用户选择商品数量的局部刷新效果，我们将商品单价从模板传入到Vue.js

```html
<script type="text/javascript">
    let sku_price = "{{ sku.price }}";
</script>
```

```js
data: {
    sku_price: sku_price,
},
```

### 2. 查询和渲染SKU规格信息

> **1.查询SKU规格信息**

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

        # 构建当前商品的规格键
        sku_specs = sku.specs.order_by('spec_id')
        sku_key = []
        for spec in sku_specs:
            sku_key.append(spec.option.id)
        # 获取当前商品的所有SKU
        skus = sku.spu.sku_set.all()
        # 构建不同规格参数（选项）的sku字典
        spec_sku_map = {}
        for s in skus:
            # 获取sku的规格参数
            s_specs = s.specs.order_by('spec_id')
            # 用于形成规格参数-sku字典的键
            key = []
            for spec in s_specs:
                key.append(spec.option.id)
            # 向规格参数-sku字典添加记录
            spec_sku_map[tuple(key)] = s.id
        # 获取当前商品的规格信息
        goods_specs = sku.spu.specs.order_by('id')
        # 若当前sku的规格信息不完整，则不再继续
        if len(sku_key) < len(goods_specs):
            return
        for index, spec in enumerate(goods_specs):
            # 复制当前sku的规格键
            key = sku_key[:]
            # 该规格的选项
            spec_options = spec.options.all()
            for option in spec_options:
                # 在规格参数sku字典中查找符合当前规格的sku
                key[index] = option.id
                option.sku_id = spec_sku_map.get(tuple(key))
            spec.spec_options = spec_options

        # 渲染页面
        context = {
            'categories':categories,
            'breadcrumb':breadcrumb,
            'sku':sku,
            'specs': goods_specs,
        }
        return render(request, 'detail.html', context)
```

> **2.渲染SKU规格信息**

```html
{% for spec in specs %}
<div class="type_select">
    <label>{{ spec.name }}:</label>
    {% for option in spec.spec_options %}
        {% if option.sku_id == sku.id %}
        <a href="javascript:;" class="select">{{ option.value }}</a>
        {% elif option.sku_id %}
        <a href="{{ url('goods:detail', args=(option.sku_id, )) }}">{{ option.value }}</a>
        {% else %}
        <a href="javascript:;">{{ option.value }}</a>
        {% endif %}
    {% endfor %}
</div>
{% endfor %}
```

### 3. 查询和渲染详情、包装和售后信息

> 商品详情、包装和售后信息被归类到商品SPU中，`sku.spu`关联查询就可以找到该`SKU`的`SPU`信息。

```html
<div class="r_wrap fr clearfix">
    <ul class="detail_tab clearfix">
        <li @click="on_tab_content('detail')" :class="tab_content.detail?'active':''">商品详情</li>
        <li @click="on_tab_content('pack')" :class="tab_content.pack?'active':''">规格与包装</li>
        <li @click="on_tab_content('service')" :class="tab_content.service?'active':''">售后服务</li>
        <li @click="on_tab_content('comment')" :class="tab_content.comment?'active':''">商品评价(18)</li>
    </ul>
    <div @click="on_tab_content('detail')" class="tab_content" :class="tab_content.detail?'current':''">
        <dl>
            <dt>商品详情：</dt>
            <dd>{{ sku.spu.desc_detail|safe }}</dd>
        </dl>
    </div>
    <div @click="on_tab_content('pack')" class="tab_content" :class="tab_content.pack?'current':''">
        <dl>
            <dt>规格与包装：</dt>
            <dd>{{ sku.spu.desc_pack|safe }}</dd>
        </dl>
    </div>
    <div @click="on_tab_content('service')" class="tab_content" :class="tab_content.service?'current':''">
        <dl>
            <dt>售后服务：</dt>
            <dd>{{ sku.spu.desc_service|safe }}</dd>
        </dl>
    </div>
    <div @click="on_tab_content('comment')" class="tab_content" :class="tab_content.comment?'current':''">
        <ul class="judge_list_con">
            {#...商品评价...#}
        </ul>
    </div>
</div>
```