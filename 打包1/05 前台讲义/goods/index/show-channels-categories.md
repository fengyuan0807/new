# 展示首页商品频道分类

### 1. 分析首页商品频道分类数据结构

<img src="/goods/images/40展示首页商品分类.png" style="zoom:50%">

```json
{
    "1":{
        "channels":[
            {"id":1, "name":"手机", "url":"http://shouji.jd.com/"},
            {"id":2, "name":"相机", "url":"http://www.itcast.cn/"}
        ],
        "sub_cats":[
            {
                "id":38, 
                "name":"手机通讯", 
                "sub_cats":[
                    {"id":115, "name":"手机"},
                    {"id":116, "name":"游戏手机"}
                ]
            },
            {
                "id":39, 
                "name":"手机配件", 
                "sub_cats":[
                    {"id":119, "name":"手机壳"},
                    {"id":120, "name":"贴膜"}
                ]
            }
        ]
    },
    "2":{
        "channels":[],
        "sub_cats":[]
    }
}
```

### 2. 查询首页商品频道分类

```python
class IndexView(View):
    """首页广告"""

    def get(self, request):
        """提供首页广告界面"""
        # 查询商品频道和分类
        categories = OrderedDict()
        channels = GoodsChannel.objects.order_by('group_id', 'sequence')
        for channel in channels:
            group_id = channel.group_id  # 当前组

            if group_id not in categories:
                categories[group_id] = {'channels': [], 'sub_cats': []}

            cat1 = channel.category  # 当前频道的类别

            # 追加当前频道
            categories[group_id]['channels'].append({
                'id': cat1.id,
                'name': cat1.name,
                'url': channel.url
            })
            # 构建当前类别的子类别
            for cat2 in cat1.subs.all():
                cat2.sub_cats = []
                for cat3 in cat2.subs.all():
                    cat2.sub_cats.append(cat3)
                categories[group_id]['sub_cats'].append(cat2)

        # 渲染模板的上下文
        context = {
            'categories': categories,
        }
        return render(request, 'index.html', context)
```

### 3. 渲染首页商品频道分类

> index.html

```html
<ul class="sub_menu">
    {% for group in categories.values() %}
    <li>
        <div class="level1">
            {% for channel in group.channels %}
            <a href="{{ channel.url }}">{{ channel.name }}</a>
            {% endfor %}
        </div>
        <div class="level2">
            {% for cat2 in group.sub_cats %}
            <div class="list_group">
                <div class="group_name fl">{{ cat2.name }} &gt;</div>
                <div class="group_detail fl">
                    {% for cat3 in cat2.sub_cats %}
                    <a href="/list/{{ cat3.id }}/1/">{{ cat3.name }}</a>
                    {% endfor %}
                </div>
            </div>
            {% endfor %}
        </div>
    </li>
    {% endfor %}
</ul>
```

### 4. 封装首页商品频道分类

> **1.封装首页商品频道分类到`contents.utils.py`文件**

```python
def get_categories():
    """
    提供商品频道和分类
    :return 菜单字典
    """
    # 查询商品频道和分类
    categories = OrderedDict()
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    for channel in channels:
        group_id = channel.group_id  # 当前组

        if group_id not in categories:
            categories[group_id] = {'channels': [], 'sub_cats': []}

        cat1 = channel.category  # 当前频道的类别

        # 追加当前频道
        categories[group_id]['channels'].append({
            'id': cat1.id,
            'name': cat1.name,
            'url': channel.url
        })
        # 构建当前类别的子类别
        for cat2 in cat1.subs.all():
            cat2.sub_cats = []
            for cat3 in cat2.subs.all():
                cat2.sub_cats.append(cat3)
            categories[group_id]['sub_cats'].append(cat2)
    return categories
```

> **2.`contents.view.py`中使用`contents.utils.py`文件**

```python
class IndexView(View):
    """首页广告"""

    def get(self, request):
        """提供首页广告界面"""
        # 查询商品频道和分类
        categories = get_categories()

        # 广告数据
        contents = {}
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        # 渲染模板的上下文
        context = {
            'categories': categories,
            'contents': contents,
        }
        return render(request, 'index.html', context)
```