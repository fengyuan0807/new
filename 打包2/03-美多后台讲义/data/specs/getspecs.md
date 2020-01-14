## 查询获取规格表列表数据

### 接口分析

**请求方式**： GET   `/meiduo_admin/goods/specs/`

**请求参数**： 通过请求头传递jwt token数据。

**返回数据**：  JSON

```json
 {
        "counts": "SPU商品规格总数量",
        "lists": [
            {
                "id": "规格id",
                "name": "规格名称",
                "spu": "SPU商品名称",
                "spu_id": "SPU商品id"
            },
            ...
          ],
          "page": "页码",
          "pages": "总页数",
          "pagesize": "页容量"
      }
```

| 返回值   | 类型 | 是否必须 | 说明       |
| -------- | ---- | -------- | ---------- |
| count    | int  | 是       | 总量       |
| lists    | 数组 | 是       | 规格表信息 |
| page     | int  | 是       | 页码       |
| pages    | int  | 是       | 总页数     |
| pagesize | int  | 是       | 页容量     |



### 后端实现

``` python
class SpecsView(ModelViewSet):

    serializer_class = SPUSpecificationSerializer
    queryset = SPUSpecification.objects.all()
    pagination_class = PageNum
```



序列化器的定义

```python
class SPUSpecificationSerializer(serializers.ModelSerializer):
  	# 关联嵌套返回spu表的商品名
    spu=serializers.StringRelatedField(read_only=True) 
    # 返回关联spu的id值
    spu_id=serializers.IntegerField()

    class Meta:
        model = SPUSpecification # 商品规格表关联了spu表的外键spu
        fields='__all__'
```

