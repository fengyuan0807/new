## 更新规格表数据

### 1、 获取要修改规格表的详情信息

点就修改按钮时，我们需要先获取要修改的规格详情信息

#### 接口分析

**请求方式**： GET ` /meiduo_admin/goods/specs/(?P<pk>\d+)/`

**请求参数**： 通过请求头传递jwt token数据。

在头部中携带要获取的规格ID

**返回数据**：  JSON

``` json
  {
        "id": "规格id",
        "name": "规格名称",
        "spu": "SPU商品名称",
        "spu_id": "SPU商品id"
    }

```

| 参数   | 类型 | 是否必须 | 说明        |
| ------ | ---- | -------- | ----------- |
| id     | int  | 是       | 规格 ID     |
| name   | str  | 是       | 规格名称    |
| spu    | str  | 是       | SPU商品名称 |
| spu_id | int  | 是       | SPU商品id   |

后端实现

``` python

# SpecsView继承的是ModelViewSet 所以获取单一规格逻辑还是使用同一个类视图
class SpecsView(ModelViewSet):
    serializer_class =SPUSpecificationSerializer
    queryset = SPUSpecification.objects.all()
    pagination_class = PageNum
```





### 2、修改规格表数据

#### 接口分析

**请求方式**： PUT   `/meiduo_admin/goods/specs/(?P<pk>\d+)/`

**请求参数**： 通过请求头传递jwt token数据。

| 参数   | 类型 | 是否必须 | 说明       |
| ------ | ---- | -------- | ---------- |
| name   | str  | 是       | 规格名称   |
| spu_id | int  | 是       | 商品SPU ID |



**返回数据**：  JSON

```json
  {
        "id": "规格id",
        "name": "规格名称",
        "goods": "SPU商品名称",
        "goods_id": "SPU商品id"
    }
```

| 参数   | 类型 | 是否必须 | 说明        |
| ------ | ---- | -------- | ----------- |
| id     | int  | 是       | 规格 ID     |
| name   | str  | 是       | 规格名称    |
| spu    | str  | 是       | SPU商品名称 |
| spu_id | int  | 是       | SPU商品id   |

后端实现

```python
# SpecsView继承的是ModelViewSet 所以修改逻辑还是使用同一个类视图
class SpecsView(ModelViewSet):
		"""
			规格表视图
		"""
    serializer_class =SPUSpecificationSerializer
    queryset = SPUSpecification.objects.all()
    pagination_class = PageNum


```

