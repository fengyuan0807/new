## 删除规格表数据

#### 接口分析

**请求方式**： Delte   `/meiduo_admin/goods/specs/(?P<pk>\d+)/`

**请求参数**： 通过请求头传递jwt token数据。

在路径中携带删除的规格的id值

**返回数据**：  JSON

返回空

后端实现

```python
# SpecsView继承的是ModelViewSet 所以删除逻辑还是使用同一个类视图
class SpecsView(ModelViewSet):
		"""
			规格表视图
		"""
    serializer_class =SPUSpecificationSerializer
    queryset = SPUSpecification.objects.all()
    pagination_class = PageNum

```

