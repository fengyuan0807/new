# Haystack扩展建立索引

> 提示：
* [Elasticsearch](https://www.elastic.co/) 的底层是开源库 [Lucene](https://lucene.apache.org/)。但是没法直接使用 Lucene，必须自己写代码去调用它的接口。

> 思考：
* 我们如何对接 Elasticsearch服务端？

> 解决方案：
* **Haystack**

### 1. Haystack介绍和安装配置

> **1.Haystack介绍**

* Haystack 是在Django中对接搜索引擎的框架，搭建了用户和搜索引擎之间的沟通桥梁。
    * 我们在Django中可以通过使用 Haystack 来调用 Elasticsearch 搜索引擎。
* Haystack 可以在不修改代码的情况下使用不同的搜索后端（比如 `Elasticsearch`、`Whoosh`、`Solr`等等）。

> **2.Haystack安装**

```bash
$ pip install django-haystack
$ pip install elasticsearch==2.4.1
```

> **3.Haystack注册应用和路由**

```python
INSTALLED_APPS = [
    'haystack', # 全文检索
]
```

```python
url(r'^search/', include('haystack.urls')),
```

> **4.Haystack配置**
* 在配置文件中配置Haystack为搜索引擎后端

```python
# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://192.168.103.158:9200/', # Elasticsearch服务器ip地址，端口号固定为9200
        'INDEX_NAME': 'meiduo_mall', # Elasticsearch建立的索引库的名称
    },
}

# 当添加、修改、删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
```

> **重要提示：**
* **HAYSTACK_SIGNAL_PROCESSOR** 配置项保证了在Django运行起来后，有新的数据产生时，Haystack仍然可以让Elasticsearch实时生成新数据的索引

### 2. Haystack建立数据索引

> **1.创建索引类**

* 通过创建索引类，来指明让搜索引擎对哪些字段建立索引，也就是可以通过哪些字段的关键字来检索数据。
* 本项目中对SKU信息进行全文检索，所以在`goods`应用中新建`search_indexes.py`文件，用于存放索引类。

```python
from haystack import indexes

from .models import SKU


class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    """SKU索引数据模型类"""
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        """返回建立索引的模型类"""
        return SKU

    def index_queryset(self, using=None):
        """返回要建立索引的数据查询集"""
        return self.get_model().objects.filter(is_launched=True)
```

* 索引类SKUIndex说明：
    * 在`SKUIndex`建立的字段，都可以借助`Haystack`由`Elasticsearch`搜索引擎查询。
    * 其中`text`字段我们声明为`document=True`，表名该字段是主要进行关键字查询的字段。
    * `text`字段的索引值可以由多个数据库模型类字段组成，具体由哪些模型类字段组成，我们用`use_template=True`表示后续通过模板来指明。

> **2.创建`text`字段索引值模板文件**

* 在`templates`目录中创建`text字段`使用的模板文件
* 具体在`templates/search/indexes/goods/sku_text.txt`文件中定义

```python
{{ object.id }}
{{ object.name }}
{{ object.caption }}
```

* 模板文件说明：当将关键词通过text参数名传递时
    * 此模板指明SKU的`id`、`name`、`caption`作为`text`字段的索引值来进行关键字索引查询。

> **3.手动生成初始索引**

```python
$ python manage.py rebuild_index
```

<img src="/goods/images/58手动建立索引.png" style="zoom:50%">

### 3. 全文检索测试

> **1.准备测试表单**

* 请求方法：`GET`
* 请求地址：`/search/`
* 请求参数：`q`

<img src="/goods/images/60搜索表单.png" style="zoom:50%">

```html
<div class="search_wrap fl">
    <form method="get" action="/search/" class="search_con">
        <input type="text" class="input_text fl" name="q" placeholder="搜索商品">
        <input type="submit" class="input_btn fr" name="" value="搜索">
    </form>
    <ul class="search_suggest fl">
        <li><a href="#">索尼微单</a></li>
        <li><a href="#">优惠15元</a></li>
        <li><a href="#">美妆个护</a></li>
        <li><a href="#">买2免1</a></li>
    </ul>
</div>
```

> **2.全文检索测试结果**

<img src="/goods/images/59全文检索测试.png" style="zoom:50%">

> 结论：
* 错误提示告诉我们在`templates/search/`目录中缺少一个`search.html`文件
* **`search.html`**文件作用就是**接收和渲染全文检索的结果**。