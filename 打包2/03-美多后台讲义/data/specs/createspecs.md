##  保存规格表数据表数据

#### 接口分析

**请求方式**：POST   `/meiduo_admin/goods/specs/`

**请求参数**： 通过请求头传递jwt token数据。

| 参数   | 类型 | 是否必须 | 说明      |
| ------ | ---- | -------- | --------- |
| name   | str  | 是       | 规格名称  |
| spu_id | int  | 是       | SPU商品id |

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
| id     | Int  | 是       | 规格id      |
| name   | Str  | 是       | 规格名称    |
| spu    | str  | 是       | SPU商品名称 |
| spu_id | Int  | 是       | spu商品id   |

后端实现

``` python
# SpecsView继承的是ModelViewSet 所以保存逻辑还是使用同一个类视图
class SpecsView(ModelViewSet):

    serializer_class =SPUSpecificationSerializer
    queryset = SPUSpecification.objects.all()
    pagination_class = PageNum
```

