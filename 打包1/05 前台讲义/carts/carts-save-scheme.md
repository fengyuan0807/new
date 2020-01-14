# 购物车存储方案

<img src="/carts/images/01添加购物车出发点.png" style="zoom:50%">
***************************************************************
<img src="/carts/images/04展示购物车1.png" style="zoom:50%">

> * 用户登录与未登录状态下，都可以保存购物车数据。
> * 用户对购物车数据的操作包括：**`增`、`删`、`改`、`查`、`全选`**等等
> * **每个用户的购物车数据都要做唯一性的标识。**

### 1. 登录用户购物车存储方案

> **1.存储数据说明**

* 如何描述一条完整的购物车记录？
    * **`用户itcast，选择了两个 iPhone8 添加到了购物车中，状态为勾选`**
* 一条完整的购物车记录包括：`用户`、`商品`、`数量`、`勾选状态`。
* **存储数据：`user_id`、`sku_id`、`count`、`selected`**

> **2.存储位置说明**

* 购物车数据量小，结构简单，更新频繁，所以我们选择内存型数据库Redis进行存储。
* **存储位置：`Redis数据库 4号库`**

```python
"carts": {
    "BACKEND": "django_redis.cache.RedisCache",
    "LOCATION": "redis://127.0.0.1:6379/4",
    "OPTIONS": {
        "CLIENT_CLASS": "django_redis.client.DefaultClient",
    }
},
```

> **3.存储类型说明**

* 提示：我们很难将**`用户、商品、数量、勾选状态`**存放到一条Redis记录中。所以我们要把购物车数据合理的分开存储。
* **用户、商品、数量：`hash`**
    * `carts_user_id: {sku_id1: count, sku_id3: count, sku_id5: count, ...}`
* **勾选状态：`set`**
    * 只将已勾选商品的sku_id存储到set中，比如，1号和3号商品是被勾选的。
    * `selected_user_id: [sku_id1, sku_id3, ...]`
    
<img src="/carts/images/02Redis存储购物车数据.png" style="zoom:50%">

> **4.存储逻辑说明**

* 当要添加到购物车的商品已存在时，对商品数量进行累加计算。
* 当要添加到购物车的商品不存在时，向hash中新增field和value即可。

### 2. 未登录用户购物车存储方案

> **1.存储数据说明**

* **存储数据：`user_id`、`sku_id`、`count`、`selected`**

> **2.存储位置说明**

* 由于用户未登录，服务端无法拿到用户的ID，所以服务端在生成购物车记录时很难唯一标识该记录。
* 我们可以将未登录用户的购物车数据缓存到用户浏览器的**`cookie`**中，每个用户自己浏览器的cookie中存储属于自己的购物车数据。
* **存储位置：`用户浏览器的cookie`**

> **3.存储类型说明**

* 提示：浏览器的cookie中存储的数据类型是字符串。
* 思考：如何在字符串中描述一条购物车记录？
* 结论：**JSON字符串**可以描述复杂结构的字符串数据，可以保证一条购物车记录不用分开存储。

```json
{
    "sku_id1":{
        "count":"1",
        "selected":"True"
    },
    "sku_id3":{
        "count":"3",
        "selected":"True"
    },
    "sku_id5":{
        "count":"3",
        "selected":"False"
    }
}
```

<img src="/carts/images/03cookie存储购物车数据1.png" style="zoom:35%">

> **4.存储逻辑说明**

* 当要添加到购物车的商品已存在时，对商品数量进行累加计算。
* 当要添加到购物车的商品不存在时，向JSON中新增field和value即可。

> **提示：**

* 浏览器cookie中存储的是字符串明文数据。
    * 我们需要对购物车这类隐私数据进行密文存储。
* 解决方案：**`pickle模块`** 和 **`base64模块`**

> **5.pickle模块介绍**

* pickle模块是Python的标准模块，提供了对Python数据的序列化操作，可以将数据转换为bytes类型，且序列化速度快。
* pickle模块使用：
    * `pickle.dumps()`将Python数据序列化为bytes类型数据。
    * `pickle.loads()`将bytes类型数据反序列化为python数据。

```python
>>> import pickle

>>> dict = {'1': {'count': 10, 'selected': True}, '2': {'count': 20, 'selected': False}}
>>> ret = pickle.dumps(dict)
>>> ret
b'\x80\x03}q\x00(X\x01\x00\x00\x001q\x01}q\x02(X\x05\x00\x00\x00countq\x03K\nX\x08\x00\x00\x00selectedq\x04\x88uX\x01\x00\x00\x002q\x05}q\x06(h\x03K\x14h\x04\x89uu.'
>>> pickle.loads(ret)
{'1': {'count': 10, 'selected': True}, '2': {'count': 20, 'selected': False}}
```

> **6.base64模块介绍**

* 提示：pickle模块序列化转换后的数据是bytes类型，浏览器cookie无法存储。
* base64模块是Python的标准模块，可以对bytes类型数据进行编码，并得到bytes类型的密文数据。
* base64模块使用：    
    * `base64.b64encode()`将bytes类型数据进行base64编码，返回编码后的bytes类型数据。
    * `base64.b64deocde()`将base64编码后的bytes类型数据进行解码，返回解码后的bytes类型数据。

```python
>>> import base64
>>> ret
b'\x80\x03}q\x00(X\x01\x00\x00\x001q\x01}q\x02(X\x05\x00\x00\x00countq\x03K\nX\x08\x00\x00\x00selectedq\x04\x88uX\x01\x00\x00\x002q\x05}q\x06(h\x03K\x14h\x04\x89uu.'
>>> b = base64.b64encode(ret)
>>> b
b'gAN9cQAoWAEAAAAxcQF9cQIoWAUAAABjb3VudHEDSwpYCAAAAHNlbGVjdGVkcQSIdVgBAAAAMnEFfXEGKGgDSxRoBIl1dS4='
>>> base64.b64decode(b)
b'\x80\x03}q\x00(X\x01\x00\x00\x001q\x01}q\x02(X\x05\x00\x00\x00countq\x03K\nX\x08\x00\x00\x00selectedq\x04\x88uX\x01\x00\x00\x002q\x05}q\x06(h\x03K\x14h\x04\x89uu.'
```

<img src="/carts/images/03cookie存储购物车数据2.png" style="zoom:35%">


