# 使用事务保存订单数据

> **重要提示：**

* 在保存订单数据时，涉及到多张表（OrderInfo、OrderGoods、SKU、SPU）的数据修改，对这些数据的修改应该是一个整体事务，即要么一起成功，要么一起失败。
* Django中对于数据库的事务，默认每执行一句数据库操作，便会自动提交。所以我们需要在保存订单中自己控制数据库事务的执行流程。

### 1. Django中事务的使用

> **1.Django中事务的使用方案**

* 在Django中可以通过**`django.db.transaction模块`**提供的**`atomic`**来定义一个事务。
* **`atomic`**提供两种方案实现事务：
    * 装饰器用法：
    
    ```python
    from django.db import transaction

    @transaction.atomic
    def viewfunc(request):
        # 这些代码会在一个事务中执行
        ......
    ```
    
    * with语句用法：
    
    ```python
    from django.db import transaction

    def viewfunc(request):
        # 这部分代码不在事务中，会被Django自动提交
        ......
    
        with transaction.atomic():
            # 这部分代码会在事务中执行
            ......
    ```

> **2.事务方案的选择：**

* **装饰器用法：**整个视图中所有MySQL数据库的操作都看做一个事务，范围太大，不够灵活。而且无法直接作用于类视图。    
* **with语句用法：**可以灵活的有选择性的把某些MySQL数据库的操作看做一个事务。而且不用关心视图的类型。
* 综合考虑后我们选择 **with语句实现事务**

> **3.事务中的保存点：**

* 在Django中，还提供了保存点的支持，可以在事务中创建保存点来记录数据的特定状态，数据库出现错误时，可以回滚到数据保存点的状态。

```python
from django.db import transaction

# 创建保存点
save_id = transaction.savepoint()  
# 回滚到保存点
transaction.savepoint_rollback(save_id)
# 提交从保存点到当前状态的所有数据库事务操作
transaction.savepoint_commit(save_id)
```

### 2. 使用事务保存订单数据

```python
class OrderCommitView(LoginRequiredJSONMixin, View):
    """订单提交"""

    def post(self, request):
        """保存订单信息和订单商品信息"""
        # 获取当前保存订单时需要的信息
        ......

        # 显式的开启一个事务
        with transaction.atomic():
            # 创建事务保存点
            save_id = transaction.savepoint()

            # 暴力回滚
            try:
                # 保存订单基本信息 OrderInfo（一）
                order = OrderInfo.objects.create(
                    order_id=order_id,
                    user=user,
                    address=address,
                    total_count=0,
                    total_amount=Decimal('0'),
                    freight=Decimal('10.00'),
                    pay_method=pay_method,
                    status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'] if pay_method == OrderInfo.PAY_METHODS_ENUM['ALIPAY'] else
                    OrderInfo.ORDER_STATUS_ENUM['UNSEND']
                )

                # 从redis读取购物车中被勾选的商品信息
                redis_conn = get_redis_connection('carts')
                redis_cart = redis_conn.hgetall('carts_%s' % user.id)
                selected = redis_conn.smembers('selected_%s' % user.id)
                carts = {}
                for sku_id in selected:
                    carts[int(sku_id)] = int(redis_cart[sku_id])
                sku_ids = carts.keys()

                # 遍历购物车中被勾选的商品信息
                for sku_id in sku_ids:
                    # 查询SKU信息
                    sku = SKU.objects.get(id=sku_id)
                    # 判断SKU库存
                    sku_count = carts[sku.id]
                    if sku_count > sku.stock:
                        # 出错就回滚
                        transaction.savepoint_rollback(save_id)
                        return http.JsonResponse({'code': RETCODE.STOCKERR, 'errmsg': '库存不足'})

                    # SKU减少库存，增加销量
                    sku.stock -= sku_count
                    sku.sales += sku_count
                    sku.save()

                    # 修改SPU销量
                    sku.spu.sales += sku_count
                    sku.spu.save()

                    # 保存订单商品信息 OrderGoods（多）
                    OrderGoods.objects.create(
                        order=order,
                        sku=sku,
                        count=sku_count,
                        price=sku.price,
                    )

                    # 保存商品订单中总价和总数量
                    order.total_count += sku_count
                    order.total_amount += (sku_count * sku.price)

                # 添加邮费和保存订单信息
                order.total_amount += order.freight
                order.save()
            except Exception as e:
                logger.error(e)
                transaction.savepoint_rollback(save_id)
                return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '下单失败'})

            # 提交订单成功，显式的提交一次事务
            transaction.savepoint_commit(save_id)

        # 清除购物车中已结算的商品
        pl = redis_conn.pipeline()
        pl.hdel('carts_%s' % user.id, *selected)
        pl.srem('selected_%s' % user.id, *selected)
        pl.execute()

        # 响应提交订单结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '下单成功', 'order_id': order.order_id})
```
