# 统计分类商品访问量

> 提示：
* 统计分类商品访问量 是统计一天内该类别的商品被访问的次数。
* 需要统计的数据，包括商品分类，访问次数，访问时间。
* 一天内，一种类别，统计一条记录。

<img src="/goods/images/68统计分类商品访问量.png" style="zoom:50%">

### 1. 统计分类商品访问量模型类

> 模型类定义在`goods.models.py`中，然后完成迁移建表。

```python
class GoodsVisitCount(BaseModel):
    """统计分类商品访问量模型类"""
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE, verbose_name='商品分类')
    count = models.IntegerField(verbose_name='访问量', default=0)
    date = models.DateField(auto_now_add=True, verbose_name='统计日期')

    class Meta:
        db_table = 'tb_goods_visit'
        verbose_name = '统计分类商品访问量'
        verbose_name_plural = verbose_name
```

### 2. 统计分类商品访问量后端逻辑

> **1.请求方式**

| 选项 | 方案 |
| ---------------- | ---------------- |
| **请求方法** | POST |
| **请求地址** | /detail/visit/(?P&lt;category_id&gt;\d+)/ |

> **2.请求参数：路径参数**

| 参数名 | 类型 | 是否必传 | 说明 |
| ---------------- | ---------------- | ---------------- | ---------------- |
| **category_id** | string | 是 | 商品分类ID，第三级分类 |

> **3.响应结果：JSON**

| 字段 | 说明 |
| ---------------- | ---------------- |
| **code** | 状态码 |
| **errmsg** | 错误信息 |

> **4.后端接口定义和实现**，
* 如果访问记录存在，说明今天不是第一次访问，不新建记录，访问量直接累加。
* 如果访问记录不存在，说明今天是第一次访问，新建记录并保存访问量。

```python
class DetailVisitView(View):
    """详情页分类商品访问量"""

    def post(self, request, category_id):
        """记录分类商品访问量"""
        try:
            category = models.GoodsCategory.objects.get(id=category_id)
        except models.GoodsCategory.DoesNotExist:
            return http.HttpResponseForbidden('缺少必传参数')

        # 获取今天的日期
        t = timezone.localtime()
        today_str = '%d-%02d-%02d' % (t.year, t.month, t.day)
        today_date = datetime.datetime.strptime(today_str, '%Y-%m-%d')
        try:
            # 查询今天该类别的商品的访问量
            counts_data = category.goodsvisitcount_set.get(date=today_date)
        except models.GoodsVisitCount.DoesNotExist:
            # 如果该类别的商品在今天没有过访问记录，就新建一个访问记录
            counts_data = models.GoodsVisitCount()

        try:
            counts_data.category = category
            counts_data.count += 1
            counts_data.save()
        except Exception as e:
            logger.error(e)
            return http.HttpResponseServerError('服务器异常')

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})
```